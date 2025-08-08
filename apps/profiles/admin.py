# Register your models here.
from django.contrib import admin

from apps.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "job_title",
        "area",
        "country",
        "availability_type",
        "created_on",
    ]
