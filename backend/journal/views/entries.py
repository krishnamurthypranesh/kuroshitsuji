import json
import logging
from typing import Optional

import constants
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from exc import InvalidEntryContent, ObjectNotFound
from helpers import generate_id, get_current_datetime
from journal.models import Collection, Entry

logger = logging.getLogger("module::journal")


@login_required
@require_http_methods(["GET", "POST"])
def entries_dispatch(request, *args, **kwargs):
    if request.method.upper() == "GET":
        params = {
            k: request.GET.get(k, None)
            for k in ["limit", "starting_after", "ending_before", "status"]
        }
        return list_entries(request, **params)

    if request.method.upper() == "POST":
        return create_entry(request, *args, **kwargs)


def create_entry(request):
    try:
        body = json.loads(request.body)
    except json.decode.JSONDecodeError as e:
        logger.error("error decoding json body")
        return JsonResponse(data={"detail": "improper data"}, status=400)

    try:
        collection = Collection.objects.get(collection_id=body.get("collection_id"))
    except Collection.DoesNotExist:
        raise ObjectNotFound("collection")

    for field in collection.template["fields"]:
        conditions = [
            field.get("required", False) == True,
            field["key"] not in body["content"],
        ]

        if all(conditions):
            raise InvalidEntryContent()

    entry_status = 10
    published_at = None
    publish = request.body.get("publish")
    if publish:
        entry_status = 20
        published_at = get_current_datetime()

    entry = Entry(
        gid=generate_id(constants.ENTRIES_PREFIX),
        user_id=request.user.id,
        collection_id=collection.id,
        content=request.content,
        status=entry_status,
        published_at=published_at,
    )

    entry.save()

    resp = {
        "collection_id": collection.gid,
        "entry_id": entry.gid,
        "content": entry.content,
        "status": Entry.EntryChoices(entry.status).name,
        "created_at": entry.created_at.replace(microsecond=0).isoformat(),
        "published_at": entry.created_at.replace(microsecond=0).isoformat(),
    }

    return JsonResponse(data=resp, status=201)


def list_entries(
    request,
    starting_after: Optional[str] = None,
    ending_before: Optional[str] = None,
    limit: int = 10,
):
    response = {
        "limit": 10,
        "records": [],
    }
    return JsonResponse(data=response, status=200)
