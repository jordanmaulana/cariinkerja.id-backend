from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.v1.filters.jobs_filter import JobsFilter
from api.v1.serializers.jobs_serializer import (
    JobAssessmentSerializer,
    JobsDetailSerializer,
    JobsListSerializer,
)
from apps.jobs.models import JobAssessment, Jobs


class JobsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class JobsAPI(viewsets.ModelViewSet):
    queryset = Jobs.objects.all().order_by("-created_on")
    pagination_class = JobsPagination
    filterset_class = JobsFilter
    permission_classes = []

    def get_serializer_class(self):
        """
        Return different serializers for list and detail operations
        """
        if self.action == "list":
            return JobsListSerializer
        return JobsDetailSerializer

    def get_queryset(self):
        """Return jobs ordered by creation date (newest first)"""
        return Jobs.objects.all().order_by("-created_on")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search in title, description, location, category, company, skills",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "source_platform",
                openapi.IN_QUERY,
                description="Filter by source platform",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "employment_type",
                openapi.IN_QUERY,
                description="Filter by employment type (full_time, part_time, contract, internship)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "work_location",
                openapi.IN_QUERY,
                description="Filter by work location (remote, onsite, hybrid)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "experience_level",
                openapi.IN_QUERY,
                description="Filter by experience level",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "job_title_category",
                openapi.IN_QUERY,
                description="Filter by job category",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "location",
                openapi.IN_QUERY,
                description="Filter by job location",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "company_name",
                openapi.IN_QUERY,
                description="Filter by company name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "hard_skills",
                openapi.IN_QUERY,
                description="Filter by hard skills",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "soft_skills",
                openapi.IN_QUERY,
                description="Filter by soft skills",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "posted_on_after",
                openapi.IN_QUERY,
                description="Filter jobs posted after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "posted_on_before",
                openapi.IN_QUERY,
                description="Filter jobs posted before this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of results per page (max 100)",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: JobsListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """List jobs with filtering and search capabilities"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={200: JobsDetailSerializer, 404: "Job not found"})
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific job by UID"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=JobsDetailSerializer,
        responses={
            200: JobsDetailSerializer,
            400: "Validation errors",
            404: "Job not found",
        },
    )
    def update(self, request, *args, **kwargs):
        """Update a job posting"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=JobsDetailSerializer,
        responses={
            200: JobsDetailSerializer,
            400: "Validation errors",
            404: "Job not found",
        },
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
        method="get",
        responses={200: "Job statistics"},
        manual_parameters=[
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter statistics by job category",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="statistics")
    def statistics(self, request):
        """Get job statistics similar to dashboard"""
        queryset = self.get_queryset()

        # Apply category filter if provided
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(job_title_category__iexact=category)

        # Calculate statistics
        total_jobs = queryset.count()

        # Employment type distribution
        employment_stats = {}
        for choice_value, choice_label in EMPLOYMENT_TYPE_CHOICES:
            count = queryset.filter(employment_type=choice_value).count()
            employment_stats[choice_value] = {
                "label": choice_label,
                "count": count,
                "percentage": round(
                    (count / total_jobs * 100) if total_jobs > 0 else 0, 2
                ),
            }

        # Work location distribution
        location_stats = {}
        for choice_value, choice_label in WORK_LOCATION_CHOICES:
            count = queryset.filter(work_location=choice_value).count()
            location_stats[choice_value] = {
                "label": choice_label,
                "count": count,
                "percentage": round(
                    (count / total_jobs * 100) if total_jobs > 0 else 0, 2
                ),
            }

        # Top categories
        categories = queryset.values("job_title_category").distinct()
        category_stats = []
        for cat in categories:
            if cat["job_title_category"]:
                count = queryset.filter(
                    job_title_category=cat["job_title_category"]
                ).count()
                category_stats.append(
                    {
                        "category": cat["job_title_category"],
                        "count": count,
                        "percentage": round(
                            (count / total_jobs * 100) if total_jobs > 0 else 0, 2
                        ),
                    }
                )

        # Sort by count and take top 10
        category_stats = sorted(category_stats, key=lambda x: x["count"], reverse=True)[
            :10
        ]

        return Response(
            {
                "total_jobs": total_jobs,
                "employment_type_distribution": employment_stats,
                "work_location_distribution": location_stats,
                "top_categories": category_stats,
            }
        )


class JobAssessmentAPI(viewsets.ModelViewSet):
    serializer_class = JobAssessmentSerializer
    pagination_class = JobsPagination

    def get_queryset(self):
        """Return assessments for the current user's profile"""
        return (
            JobAssessment.objects.filter(profile__actor=self.request.user)
            .select_related("job", "profile")
            .order_by("-created_on")
        )

    @swagger_auto_schema(responses={200: JobAssessmentSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        """List job assessments for the current user"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=JobAssessmentSerializer,
        responses={201: JobAssessmentSerializer, 400: "Validation errors"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new job assessment"""
        # Get user's profile
        try:
            from apps.profiles.models import Profile

            profile = Profile.objects.get(actor=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found. Please create a profile first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile, actor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
