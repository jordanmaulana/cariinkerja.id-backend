from bson import objectid
from django.contrib.auth.models import User
from django.db import models


def make_object_id():
    return str(objectid.ObjectId())


class BaseModel(models.Model):
    uid = models.CharField(default=make_object_id, db_index=True, max_length=32)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        ordering = ["-uid"]
        indexes = [models.Index(fields=["created_on"])]

    def __str__(self):
        return self.uid
