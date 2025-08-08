from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.profiles.models import Profile


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="old_password"
        )
        self.profile = Profile.objects.create(
            actor=self.user, name="Test User", phone_number="1234567890"
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        url = "/api/v1/profile/change-password/"
        data = {"old_password": "old_password", "new_password": "new_password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    def test_change_password_wrong_old_password(self):
        url = "/api/v1/profile/change-password/"
        data = {"old_password": "wrong_password", "new_password": "new_password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_missing_fields(self):
        url = "/api/v1/profile/change-password/"
        data = {"old_password": "old_password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
