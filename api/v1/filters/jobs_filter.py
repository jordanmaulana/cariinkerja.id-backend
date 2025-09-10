from django.db.models import Q
from django_filters import rest_framework as filters

from apps.jobs.consts import EMPLOYMENT_TYPE_CHOICES, WORK_LOCATION_CHOICES
from apps.jobs.models import Jobs


class JobsFilter(filters.FilterSet):
    # Text search across multiple fields (similar to admin search_fields)
    search = filters.CharFilter(method="filter_search", label="Search")

    # Exact match filters (similar to admin list_filter)
    source_platform = filters.CharFilter(
        field_name="source_platform", lookup_expr="iexact"
    )
    employment_type = filters.ChoiceFilter(choices=EMPLOYMENT_TYPE_CHOICES)
    work_location = filters.ChoiceFilter(choices=WORK_LOCATION_CHOICES)
    experience_level = filters.CharFilter(
        field_name="experience_level", lookup_expr="icontains"
    )
    job_title_category = filters.CharFilter(
        field_name="job_title_category", lookup_expr="iexact"
    )

    # Date range filters
    posted_on_after = filters.DateTimeFilter(field_name="posted_on", lookup_expr="gte")
    posted_on_before = filters.DateTimeFilter(field_name="posted_on", lookup_expr="lte")
    created_on_after = filters.DateTimeFilter(
        field_name="created_on", lookup_expr="gte"
    )
    created_on_before = filters.DateTimeFilter(
        field_name="created_on", lookup_expr="lte"
    )

    # Location and company filters
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")
    company_name = filters.CharFilter(
        field_name="company_name", lookup_expr="icontains"
    )

    # Skills filters
    hard_skills = filters.CharFilter(method="filter_hard_skills", label="Hard Skills")
    soft_skills = filters.CharFilter(method="filter_soft_skills", label="Soft Skills")

    class Meta:
        model = Jobs
        fields = [
            "search",
            "source_platform",
            "employment_type",
            "work_location",
            "experience_level",
            "job_title_category",
            "posted_on_after",
            "posted_on_before",
            "created_on_after",
            "created_on_before",
            "location",
            "company_name",
            "hard_skills",
            "soft_skills",
        ]

    def filter_search(self, queryset, name, value):
        """Search across multiple fields like admin search_fields"""
        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(location__icontains=value)
            | Q(job_title_category__icontains=value)
            | Q(company_name__icontains=value)
            | Q(hard_skills__icontains=value)
            | Q(soft_skills__icontains=value)
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
