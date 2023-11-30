import uuid

from django.db import models

from helpers import generate_id


class CustomBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    gid = models.CharField(max_length=50, default=generate_id, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
