from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone

from common import CustomBaseModel


class UserManager(BaseUserManager):
    def _create_user(self, username, **extra_fields):
        now = timezone.now()
        username = self.normalize_email(username)

        user = self.model(
            username=username,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            joined_at=now,
            **extra_fields
        )
        user.save(using=self._db)

        return user

    def create_user(self, username, **extra_fields):
        return self._create_user(username, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        return user


class User(AbstractBaseUser, CustomBaseModel, PermissionsMixin):
    username = models.CharField(max_length=100, null=False, unique=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(null=True, blank=True)

    # unused fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "username"

    objects = UserManager()


class UserSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(null=False, blank=False)
    session_id = models.CharField(
        max_length=255, null=False, blank=False, db_index=True
    )
    session_data = models.CharField(max_length=4096, null=False, blank=True)
    expires_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_sessions"
