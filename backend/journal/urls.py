from django.urls import path
from journal import views

urlpatterns = [
    path("collections/", views.create_collection, name="create_collection"),
    path(
        "collections/<str:collection_id>/",
        views.get_collection,
        name="get_collection_by_id",
    ),
]
