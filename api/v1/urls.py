from django.urls import include, path
from rest_framework import routers

from api.v1.api.auth_api import AuthAPI
from api.v1.api.profile_api import ProfileAPI

api_router = routers.DefaultRouter()
api_router.register(r"auth", AuthAPI, basename="auth")
api_router.register(r"profile", ProfileAPI, basename="profile")

urlpatterns = [
    path("", include(api_router.urls)),
    path(
        "auth/reset-password/<uidb64>/<token>/",
        AuthAPI.as_view({"post": "reset_password"}),
        name="password-reset-confirm",
    ),
]
