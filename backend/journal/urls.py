from django.urls import path
from journal.views import collections, entries

urlpatterns = [
    path(
        "collections/", collections.collections_dispatcher, name="dispatch_collections"
    ),
    path(
        "collections/<str:collection_id>/",
        collections.get_collection,
        name="get_collection_by_id",
    ),
    path("entries/", entries.entries_dispatch, name="dispatch_entries"),
    path(
        "entries/<str:entry_id>/",
        entries.get_entry,
        name="get_entry_by_id",
    ),
]
