# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

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
        user_count = Profile.objects.all().count()
        users_registered_today = Profile.objects.filter(created_on=today).count()

        return render(
            request,
            "dashboard.html",
            context={
                "user_count": user_count,
                "users_registered_today": users_registered_today,
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
