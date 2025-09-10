from django.db.models import Q
from django_filters import rest_framework as filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.v1.serializers.jobs_serializer import JobsSerializer, JobAssessmentSerializer
from apps.jobs.models import Jobs, JobAssessment
from apps.jobs.consts import EMPLOYMENT_TYPE_CHOICES, WORK_LOCATION_CHOICES


class JobsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobsFilter(filters.FilterSet):
    # Text search across multiple fields (similar to admin search_fields)
    search = filters.CharFilter(method='filter_search', label='Search')
    
    # Exact match filters (similar to admin list_filter)
    source_platform = filters.CharFilter(field_name='source_platform', lookup_expr='iexact')
    employment_type = filters.ChoiceFilter(choices=EMPLOYMENT_TYPE_CHOICES)
    work_location = filters.ChoiceFilter(choices=WORK_LOCATION_CHOICES)
    experience_level = filters.CharFilter(field_name='experience_level', lookup_expr='icontains')
    job_title_category = filters.CharFilter(field_name='job_title_category', lookup_expr='iexact')
    
    # Date range filters
    posted_on_after = filters.DateTimeFilter(field_name='posted_on', lookup_expr='gte')
    posted_on_before = filters.DateTimeFilter(field_name='posted_on', lookup_expr='lte')
    created_on_after = filters.DateTimeFilter(field_name='created_on', lookup_expr='gte')
    created_on_before = filters.DateTimeFilter(field_name='created_on', lookup_expr='lte')
    
    # Location and company filters
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    company_name = filters.CharFilter(field_name='company_name', lookup_expr='icontains')
    
    # Skills filters
    hard_skills = filters.CharFilter(method='filter_hard_skills', label='Hard Skills')
    soft_skills = filters.CharFilter(method='filter_soft_skills', label='Soft Skills')
    
    class Meta:
        model = Jobs
        fields = [
            'search',
            'source_platform',
            'employment_type', 
            'work_location',
            'experience_level',
            'job_title_category',
            'posted_on_after',
            'posted_on_before',
            'created_on_after',
            'created_on_before',
            'location',
            'company_name',
            'hard_skills',
            'soft_skills',
        ]
    
    def filter_search(self, queryset, name, value):
        """Search across multiple fields like admin search_fields"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(location__icontains=value) |
            Q(job_title_category__icontains=value) |
            Q(company_name__icontains=value) |
            Q(hard_skills__icontains=value) |
            Q(soft_skills__icontains=value)
        )
    
    def filter_hard_skills(self, queryset, name, value):
        """Filter jobs that contain specific hard skills"""
        if not value:
            return queryset
        return queryset.filter(hard_skills__icontains=value)
    
    def filter_soft_skills(self, queryset, name, value):
        """Filter jobs that contain specific soft skills"""
        if not value:
            return queryset
        return queryset.filter(soft_skills__icontains=value)


class JobsAPI(viewsets.ModelViewSet):
    queryset = Jobs.objects.all().order_by('-created_on')
    serializer_class = JobsSerializer
    pagination_class = JobsPagination
    filterset_class = JobsFilter
    permission_classes = []
    
    def get_queryset(self):
        """Return jobs ordered by creation date (newest first)"""
        return Jobs.objects.all().order_by('-created_on')
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description='Search in title, description, location, category, company, skills', type=openapi.TYPE_STRING),
            openapi.Parameter('source_platform', openapi.IN_QUERY, description='Filter by source platform', type=openapi.TYPE_STRING),
            openapi.Parameter('employment_type', openapi.IN_QUERY, description='Filter by employment type (full_time, part_time, contract, internship)', type=openapi.TYPE_STRING),
            openapi.Parameter('work_location', openapi.IN_QUERY, description='Filter by work location (remote, onsite, hybrid)', type=openapi.TYPE_STRING),
            openapi.Parameter('experience_level', openapi.IN_QUERY, description='Filter by experience level', type=openapi.TYPE_STRING),
            openapi.Parameter('job_title_category', openapi.IN_QUERY, description='Filter by job category', type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY, description='Filter by job location', type=openapi.TYPE_STRING),
            openapi.Parameter('company_name', openapi.IN_QUERY, description='Filter by company name', type=openapi.TYPE_STRING),
            openapi.Parameter('hard_skills', openapi.IN_QUERY, description='Filter by hard skills', type=openapi.TYPE_STRING),
            openapi.Parameter('soft_skills', openapi.IN_QUERY, description='Filter by soft skills', type=openapi.TYPE_STRING),
            openapi.Parameter('posted_on_after', openapi.IN_QUERY, description='Filter jobs posted after this date (YYYY-MM-DD)', type=openapi.TYPE_STRING),
            openapi.Parameter('posted_on_before', openapi.IN_QUERY, description='Filter jobs posted before this date (YYYY-MM-DD)', type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description='Number of results per page (max 100)', type=openapi.TYPE_INTEGER),
        ],
        responses={200: JobsSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List jobs with filtering and search capabilities"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        responses={200: JobsSerializer, 404: "Job not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific job by UID"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=JobsSerializer,
        responses={201: JobsSerializer, 400: "Validation errors"}
    )
    def create(self, request, *args, **kwargs):
        """Create a new job posting"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(actor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=JobsSerializer,
        responses={200: JobsSerializer, 400: "Validation errors", 404: "Job not found"}
    )
    def update(self, request, *args, **kwargs):
        """Update a job posting"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=JobsSerializer,
        responses={200: JobsSerializer, 400: "Validation errors", 404: "Job not found"}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a job posting"""
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        responses={204: "Job deleted successfully", 404: "Job not found"}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a job posting"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='get',
        responses={200: 'Job statistics'},
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description='Filter statistics by job category', type=openapi.TYPE_STRING),
        ]
    )
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """Get job statistics similar to dashboard"""
        queryset = self.get_queryset()
        
        # Apply category filter if provided
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(job_title_category__iexact=category)
        
        # Calculate statistics
        total_jobs = queryset.count()
        
        # Employment type distribution
        employment_stats = {}
        for choice_value, choice_label in EMPLOYMENT_TYPE_CHOICES:
            count = queryset.filter(employment_type=choice_value).count()
            employment_stats[choice_value] = {
                'label': choice_label,
                'count': count,
                'percentage': round((count / total_jobs * 100) if total_jobs > 0 else 0, 2)
            }
        
        # Work location distribution
        location_stats = {}
        for choice_value, choice_label in WORK_LOCATION_CHOICES:
            count = queryset.filter(work_location=choice_value).count()
            location_stats[choice_value] = {
                'label': choice_label,
                'count': count,
                'percentage': round((count / total_jobs * 100) if total_jobs > 0 else 0, 2)
            }
        
        # Top categories
        categories = queryset.values('job_title_category').distinct()
        category_stats = []
        for cat in categories:
            if cat['job_title_category']:
                count = queryset.filter(job_title_category=cat['job_title_category']).count()
                category_stats.append({
                    'category': cat['job_title_category'],
                    'count': count,
                    'percentage': round((count / total_jobs * 100) if total_jobs > 0 else 0, 2)
                })
        
        # Sort by count and take top 10
        category_stats = sorted(category_stats, key=lambda x: x['count'], reverse=True)[:10]
        
        return Response({
            'total_jobs': total_jobs,
            'employment_type_distribution': employment_stats,
            'work_location_distribution': location_stats,
            'top_categories': category_stats,
        })


class JobAssessmentAPI(viewsets.ModelViewSet):
    serializer_class = JobAssessmentSerializer
    pagination_class = JobsPagination
    
    def get_queryset(self):
        """Return assessments for the current user's profile"""
        return JobAssessment.objects.filter(
            profile__actor=self.request.user
        ).select_related('job', 'profile').order_by('-created_on')
    
    @swagger_auto_schema(
        responses={200: JobAssessmentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List job assessments for the current user"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        request_body=JobAssessmentSerializer,
        responses={201: JobAssessmentSerializer, 400: "Validation errors"}
    )
    def create(self, request, *args, **kwargs):
        """Create a new job assessment"""
        # Get user's profile
        try:
            from apps.profiles.models import Profile
            profile = Profile.objects.get(actor=request.user)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Profile not found. Please create a profile first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile, actor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)