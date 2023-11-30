import json
import logging
from datetime import timedelta

from authn.models import UserSession
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from helpers import generate_session_id, get_current_datetime

logger = logging.getLogger("module::authn")


@require_http_methods(["POST"])
def create_session(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        logger.error("error decoding json body")
        return JsonResponse(data={"detail": "improper data"}, status=400)

    username = body.get("username")
    password = body.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)

        user_session = UserSession(
            user_id=user.id,
            session_id=generate_session_id(),
            expires_at=get_current_datetime() + timedelta(days=3),
        )
        user_session.save()

        return JsonResponse(data={"token": user_session.session_id}, status=201)

    return JsonResponse(data={"detail": "failure"}, status=401)
