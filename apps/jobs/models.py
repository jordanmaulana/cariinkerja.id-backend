from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from core.models import BaseModel

from .consts import EMPLOYMENT_TYPE_CHOICES, WORK_LOCATION_CHOICES, SOURCE_PLATFORM_CHOICES


# Create your models here.
class Jobs(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(unique=True)
    hard_skills = ArrayField(
        models.CharField(max_length=255), size=20, null=True, blank=True, default=list
    )
    soft_skills = ArrayField(
        models.CharField(max_length=255), size=20, null=True, blank=True, default=list
    )
    experience_level = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    employment_type = models.CharField(
        max_length=255,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="full_time",
    )
    work_location = models.CharField(
        max_length=255,
        choices=WORK_LOCATION_CHOICES,
        default="remote",
    )
    job_title_category = models.CharField(max_length=255, default="other")
    posted_on = models.DateTimeField(default=timezone.now, blank=True, null=True)
    requirements = ArrayField(
        models.CharField(max_length=800), size=20, null=True, blank=True, default=list
    )
    company_name = models.CharField(max_length=255, null=True, blank=True)
    source_platform = models.CharField(
        max_length=255,
        choices=SOURCE_PLATFORM_CHOICES,
        default="weworkremotely.com",
    )

    def __str__(self):
        return self.title


class JobAssessment(BaseModel):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    profile = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    summary = models.TextField()
    hard_skill_gap = ArrayField(
        models.CharField(max_length=255), size=20, null=True, blank=True, default=list
    )
    soft_skill_gap = ArrayField(
        models.CharField(max_length=255), size=20, null=True, blank=True, default=list
    )
    score = models.IntegerField(default=0)
