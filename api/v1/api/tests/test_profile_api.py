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
            actor=self.user,
            name="Test User",
            job_title="Software Developer",
            area="SE_ASIA",
            availability_type="REMOTE",
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

    def test_get_profile_success(self):
        url = "/api/v1/profile/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test User")
        self.assertEqual(response.data["job_title"], "Software Developer")
        self.assertEqual(response.data["area"], "SE_ASIA")
        self.assertEqual(response.data["availability_type"], "REMOTE")

    def test_update_profile_success(self):
        url = f"/api/v1/profile/{self.profile.uid}/"
        data = {
            "name": "Updated Name",
            "job_title": "Senior Developer",
            "linkedin_url": "https://linkedin.com/in/testuser",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, "Updated Name")
        self.assertEqual(self.profile.job_title, "Senior Developer")
        self.assertEqual(self.profile.linkedin_url, "https://linkedin.com/in/testuser")

    def test_delete_profile_success(self):
        url = f"/api/v1/profile/{self.profile.uid}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.deleted_on)
