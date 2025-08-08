from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.profile_serializer import (
    ChangePasswordSerializer,
    ProfileSerializer,
)
from apps.profiles.models import Profile


class ProfileAPI(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(actor=self.request.user)

    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={200: "Profile updated successfully"},
    )
    def update(self, request, pk=None):
        try:
            profile = self.get_queryset().get(uid=pk)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            profile = self.get_queryset().get(uid=pk)
            profile.deleted_on = datetime.now()
            profile.obfuscate_email()
            profile.save()
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Profile deleted successfully"}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        method="post",
        request_body=ChangePasswordSerializer,
        responses={200: "Password changed successfully", 400: "Invalid password"},
    )
    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
