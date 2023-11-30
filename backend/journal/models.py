from django.db import models

from common import CustomBaseModel

class Collection(CustomBaseModel):
    user_id = models.BigIntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    # this is a good candidate for FormIO
    # TODO: replace dictionary with a type that can be serialized to FormIO when returning the response
    template = models.JSONField(null=False, blank=False)
    active = models.BooleanField(null=False, default=False)
    published_entries_count = models.IntegerField(null=False, default=0)


class Entry(CustomBaseModel):
    collection_id = models.BigIntegerField(null=False, blank=False)
    content = models.JSONField(null=False, default={})
    template = models.JSONField(null=False, blank=False)
    is_draft = models.BooleanField(null=False, default=False)
    published_at = models.DatetimeField(null=True)
