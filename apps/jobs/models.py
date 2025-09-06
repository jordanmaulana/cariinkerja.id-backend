from django.db import models
from django.utils import timezone

from core.models import BaseModel
from .consts import EMPLOYMENT_TYPE_CHOICES, WORK_LOCATION_CHOICES


# Create your models here.
class Jobs(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(unique=True)
    hard_skills = models.TextField(null=True, blank=True)
    soft_skills = models.TextField(null=True, blank=True)
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
    posted_on = models.DateTimeField(default=timezone.now)

class JobAssessment(BaseModel):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    profile = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    summary = models.TextField()
    hard_skill_gap = models.TextField()
    soft_skill_gap = models.TextField()
    