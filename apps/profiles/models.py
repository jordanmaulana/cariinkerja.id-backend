import uuid

from django.db import models

from core.models import BaseModel


# Create your models here.
class Profile(BaseModel):
    name = models.CharField(max_length=255)
    deleted_on = models.DateTimeField(blank=True, null=True)

    def obfuscate_email(self):
        if self.actor:
            self.actor.username = f"deleted_{uuid.uuid4()}"
            self.actor.email = f"deleted_{uuid.uuid4()}@example.com"
            self.actor.save()

    def __str__(self):
        return self.name
