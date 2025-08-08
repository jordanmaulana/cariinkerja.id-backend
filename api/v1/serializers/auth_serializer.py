from django.contrib.auth.models import User
from rest_framework import serializers

from apps.profiles.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "name"]


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email ini sudah terdaftar.")
        return value

    def create(self, validated_data) -> User:
        name = validated_data.pop("name")
        email = validated_data.get("email")

        # Create user and use email as username
        user = User.objects.create_user(
            username=email, email=email, password=validated_data.get("password")
        )

        # Create profile using BaseModel.actor as a link
        Profile.objects.create(name=name, actor=user)

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]
