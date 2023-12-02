from authn import views
from django.urls import path

urlpatterns = [
    path("user-sessions/", views.UserSessions.as_view(), name="user_sessions"),
]
