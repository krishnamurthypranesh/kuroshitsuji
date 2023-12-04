from common import CustomBaseModel
from django.db import models


class Collection(CustomBaseModel):
    user_id = models.BigIntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    # this is a good candidate for FormIO
    # TODO: replace dictionary with a type that can be serialized to FormIO when returning the response
    template = models.JSONField(null=False, blank=False)
    # TODO: replace this with a status field to capture more information
    active = models.BooleanField(null=False, default=False)
    published_entries_count = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = "collections"


class Entry(CustomBaseModel):
    class EntryChoices(models.IntegerChoices):
        INIT = 0
        DRAFT = 10
        PUBLISHED = 20
        INACTIVE = 30

    user_id = models.BigIntegerField(null=False, blank=False)
    collection_id = models.BigIntegerField(null=False, blank=False)
    content = models.JSONField(null=False, default=dict)
    status = models.IntegerField(
        null=False, choices=EntryChoices.choices, default=EntryChoices.DRAFT
    )
    published_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "entries"
