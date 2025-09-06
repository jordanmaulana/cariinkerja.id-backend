from django.db import models

from core.models import BaseModel


# Create your models here.
class Jobs(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(unique=True)
    hard_skills = models.TextField(null=True, blank=True)
    soft_skills = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    employment_type = (
        models.CharField(
            max_length=255,
            choices=[
                ("full_time", "Full Time"),
                ("part_time", "Part Time"),
                ("contract", "Contract"),
                ("internship", "Internship"),
            ],
        ),
    )
    work_location = (
        models.CharField(
            max_length=255,
            choices=[
                ("remote", "Remote"),
                ("onsite", "Onsite"),
                ("hybrid", "Hybrid"),
            ],
        ),
    )

class JobAssessment(BaseModel):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    profile = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    summary = models.TextField()
    hard_skill_gap = models.TextField()
    soft_skill_gap = models.TextField()
    