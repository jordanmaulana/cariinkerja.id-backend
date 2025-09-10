# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.db.models import Avg, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from apps.jobs.models import JobAssessment, Jobs
from apps.profiles.models import Profile
from core.forms import CustomSetPasswordForm


class SuperuserRequiredMixin(View):
    @method_decorator(
        user_passes_test(lambda user: user.is_superuser, login_url="/login/")
    )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DashboardView(SuperuserRequiredMixin, View):
    def get(self, request):
        """
        Render the index page for the dashboard.
        """
        today = timezone.now().date()

        # User statistics
        user_count = Profile.objects.all().count()
        users_registered_today = Profile.objects.filter(created_on=today).count()

        # Job statistics
        total_jobs = Jobs.objects.all().count()
        jobs_posted_today = Jobs.objects.filter(created_on__date=today).count()

        # Employment type distribution
        employment_type_stats = (
            Jobs.objects.values("employment_type")
            .annotate(count=Count("employment_type"))
            .order_by("-count")
        )

        # Work location distribution
        work_location_stats = (
            Jobs.objects.values("work_location")
            .annotate(count=Count("work_location"))
            .order_by("-count")
        )

        # Job category distribution
        job_category_stats = (
            Jobs.objects.values("job_title_category")
            .annotate(count=Count("job_title_category"))
            .order_by("-count")[:5]
        )  # Top 5 categories

        # Source platform distribution
        source_platform_stats = (
            Jobs.objects.values("source_platform")
            .annotate(count=Count("source_platform"))
            .order_by("-count")
        )

        # Job assessment statistics
        total_assessments = JobAssessment.objects.all().count()
        assessments_today = JobAssessment.objects.filter(created_on__date=today).count()

        # Average assessment score
        avg_assessment_score = (
            JobAssessment.objects.aggregate(avg_score=Avg("score"))["avg_score"] or 0
        )

        return render(
            request,
            "dashboard.html",
            context={
                "user_count": user_count,
                "users_registered_today": users_registered_today,
                "total_jobs": total_jobs,
                "jobs_posted_today": jobs_posted_today,
                "employment_type_stats": employment_type_stats,
                "work_location_stats": work_location_stats,
                "job_category_stats": job_category_stats,
                "source_platform_stats": source_platform_stats,
                "total_assessments": total_assessments,
                "assessments_today": assessments_today,
                "avg_assessment_score": round(avg_assessment_score, 1),
            },
        )


class AdminLoginView(LoginView):
    template_name = "login_view.html"
    success_url = "/dashboard/"


class PasswordResetDoneView(TemplateView):
    template_name = "password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "reset_password.html"
    success_url = reverse_lazy("password_reset_done")
    form_class = CustomSetPasswordForm
