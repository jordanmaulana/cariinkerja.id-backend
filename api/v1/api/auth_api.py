from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers.auth_serializer import LoginSerializer, RegisterSerializer
from api.v1.serializers.password_reset_serializer import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from core.settings import BACKEND_URL, EMAIL_HOST_USER


class AuthAPI(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        request_body=RegisterSerializer,
        responses={200: "Pengguna berhasil terdaftar"},
    )
    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "Pengguna berhasil terdaftar", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="post", request_body=LoginSerializer, responses={200: "Masuk berhasil"}
    )
    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(username=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(
            {"error": "Email atau kata sandi salah"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @swagger_auto_schema(
        method="post",
        request_body=PasswordResetRequestSerializer,
        responses={200: "Tautan reset kata sandi terkirim"},
    )
    @action(detail=False, methods=["post"], url_path="forgot-password")
    def forgot_password(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{BACKEND_URL}/reset-password/{uid}/{token}/"

            html_message = render_to_string(
                "password_reset_email.html", {"reset_link": reset_link}
            )
            send_mail(
                "Permintaan Reset Kata Sandi",
                f"Klik tautan untuk mereset kata sandi Anda: {reset_link}",
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message,
            )
        return Response({"message": "Tautan reset kata sandi terkirim"})

    @swagger_auto_schema(
        method="post",
        request_body=PasswordResetSerializer,
        responses={200: "Reset kata sandi berhasil"},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)",
    )
    def reset_password(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"message": "Reset kata sandi berhasil"})
        else:
            return Response(
                {"error": "Token tidak valid"}, status=status.HTTP_400_BAD_REQUEST
            )
