import logging
from datetime import timezone

from authn.models import User, UserSession
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
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
                return JsonResponse(data={"detail": "session expired"}, status=440)

            user = User.objects.get(id=user_session.user_id)

            request.user = user


class ExceptionHandlingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        try:
            return view_func(request)
        except Exception as e:
            logging.error(f"error: {e} when processing request")
            error_message = getattr(e, "err_msg", str(e))
            status_code = getattr(e, "status_code", 500)

            return JsonResponse(data={"detail": error_message}, status=status_code)
