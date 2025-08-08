from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="actor.email", read_only=True)
    username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "uid",
            "name", 
            "profile",
            "linkedin_url",
            "job_title",
            "area",
            "country",
            "availability_type",
            "created_on",
            "updated_on",
            "email",
            "username"
        ]
        read_only_fields = ["uid", "created_on", "updated_on"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password lama salah.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
