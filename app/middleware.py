from datetime import timezone

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from authn.models import User, UserSession
from exc import ExpiredUserSessionExcpetion
from helpers import get_current_datetime


class AuthenticationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            if request.path_info.lstrip("/") not in ["v1/authn/user-sessions/"]:
                return JsonResponse(data={"detail": "Unauthorized"}, status=401)
            else:
                return None

        else:
            _, token = auth_header.split(" ")
            user_session = UserSession.objects.get(session_id=token)

            if (
                user_session.expires_at.astimezone(timezone.utc)
                < get_current_datetime()
            ):
                raise ExpiredUserSessionExcpetion()

            user = User.objects.get(id=user_session.user_id)

            request.user = user
