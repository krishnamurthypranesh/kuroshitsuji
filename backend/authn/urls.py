from django.urls import path

from authn import views

urlpatterns = [
    path("user-sessions/", views.create_session, name="create_session"),
]
