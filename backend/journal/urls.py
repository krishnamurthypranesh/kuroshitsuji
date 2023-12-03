from django.urls import path
from journal.views import collections

urlpatterns = [
    path(
        "collections/", collections.collections_dispatcher, name="dispatch_collections"
    ),
    path(
        "collections/<str:collection_id>/",
        collections.get_collection,
        name="get_collection_by_id",
    ),
]
