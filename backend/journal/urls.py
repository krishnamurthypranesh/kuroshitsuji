from django.urls import path
from journal import views

urlpatterns = [
    path("collections/", views.collections_dispatcher, name="dispatch_collections"),
    path(
        "collections/<str:collection_id>/",
        views.get_collection,
        name="get_collection_by_id",
    ),
]
