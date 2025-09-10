from datetime import datetime, timedelta

from django.db.models import Q
from django.views.generic import DetailView, ListView

from .consts import EMPLOYMENT_TYPE_CHOICES, WORK_LOCATION_CHOICES
from .models import Jobs


class JobListView(ListView):
    model = Jobs
    template_name = "job_list.html"
    context_object_name = "jobs"
    paginate_by = 20
    ordering = ["-posted_on"]

    def get_queryset(self):
        queryset = Jobs.objects.all()

        # Filter by employment type
        employment_type = self.request.GET.get("employment_type")
        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)

        # Filter by work location
        work_location = self.request.GET.get("work_location")
        if work_location:
            queryset = queryset.filter(work_location=work_location)

        # Filter by experience level
        experience_level = self.request.GET.get("experience_level")
        if experience_level:
            queryset = queryset.filter(experience_level__icontains=experience_level)

        # Filter by job title category
        job_title_category = self.request.GET.get("job_title_category")
        if job_title_category:
            queryset = queryset.filter(job_title_category__icontains=job_title_category)

        # Filter by date posted
        date_filter = self.request.GET.get("posted_on")
        if date_filter:
            if date_filter == "today":
                queryset = queryset.filter(posted_on__date=datetime.now().date())
            elif date_filter == "week":
                week_ago = datetime.now() - timedelta(days=7)
                queryset = queryset.filter(posted_on__gte=week_ago)
            elif date_filter == "month":
                month_ago = datetime.now() - timedelta(days=30)
                queryset = queryset.filter(posted_on__gte=month_ago)

        # Search functionality
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(location__icontains=search)
                | Q(company_name__icontains=search)
            )

        return queryset.order_by("-posted_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employment_type_choices"] = EMPLOYMENT_TYPE_CHOICES
        context["work_location_choices"] = WORK_LOCATION_CHOICES
        context["current_filters"] = {
            "employment_type": self.request.GET.get("employment_type", ""),
            "work_location": self.request.GET.get("work_location", ""),
            "experience_level": self.request.GET.get("experience_level", ""),
            "job_title_category": self.request.GET.get("job_title_category", ""),
            "posted_on": self.request.GET.get("posted_on", ""),
            "search": self.request.GET.get("search", ""),
        }
        return context


class JobDetailView(DetailView):
    model = Jobs
    template_name = "job_detail.html"
    context_object_name = "job"
    slug_field = "uid"
    slug_url_kwarg = "uid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve query parameters for back button
        context["back_url_params"] = self.request.GET.urlencode()
        return context
