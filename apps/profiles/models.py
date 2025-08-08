import uuid

from django.db import models

from core.models import BaseModel
from .constants import (
    AREA_CHOICES, 
    AVAILABILITY_TYPE_CHOICES,
    AREA_DEFAULT,
    AVAILABILITY_TYPE_DEFAULT
)


# Create your models here.
class Profile(BaseModel):
    name = models.CharField(max_length=255)
    profile = models.TextField(blank=True, null=True)
    linkedin_url = models.CharField(max_length=255, blank=True, null=True)
    deleted_on = models.DateTimeField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(
        max_length=50,
        choices=AREA_CHOICES,
        default=AREA_DEFAULT
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    availability_type = models.CharField(
        max_length=20,
        choices=AVAILABILITY_TYPE_CHOICES,
        default=AVAILABILITY_TYPE_DEFAULT
    )

    def obfuscate_email(self):
        if self.actor:
            self.actor.username = f"deleted_{uuid.uuid4()}"
            self.actor.email = f"deleted_{uuid.uuid4()}@example.com"
            self.actor.save()

    def __str__(self):
        return self.name
