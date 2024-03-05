import json
import logging
from typing import Optional

import constants
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from exc import (
    BadPaginationParameter,
    InactiveCollectionEntryAddition,
    InvalidEntryContent,
    ObjectNotFound,
)
from helpers import generate_id, get_current_datetime
from journal.models import Collection, Entry
from journal.schema import EntryOut, ListEntriesResponse

logger = logging.getLogger("module::journal")


@login_required
@require_http_methods(["GET", "POST"])
def entries_dispatch(request, *args, **kwargs):
    if request.method.upper() == "GET":
        params = {
            k: request.GET.get(k, None)
            for k in ["limit", "starting_after", "ending_before", "collection_id"]
        }
        return list_entries(request, **params)

    if request.method.upper() == "POST":
        return create_entry(request, *args, **kwargs)


def create_entry(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        logger.error(request.body)
        logger.error(f"error: {e} decoding json body")
        return JsonResponse(data={"detail": "improper data"}, status=400)

    try:
        collection = Collection.objects.get(gid=body.get("collection_id"))
    except Collection.DoesNotExist:
        raise ObjectNotFound("collection")

    if not collection.active:
        raise InactiveCollectionEntryAddition()

    if not body.get("title"):
        raise InvalidEntryContent("title not supplied")

    for field in collection.template["fields"]:
        conditions = [
            field.get("required", False) == True,
            field["key"] not in body["content"],
        ]

        if all(conditions):
            raise InvalidEntryContent()

    entry_status = 10
    published_at = None
    publish = body.get("publish")
    if publish:
        entry_status = 20
        published_at = get_current_datetime()

    entry = Entry(
        gid=generate_id(constants.ENTRIES_PREFIX),
        user_id=request.user.id,
        collection_id=collection.id,
        title=body["title"],
        content=body["content"],
        status=entry_status,
        published_at=published_at,
    )

    entry.save()

    resp = {
        "collection_id": collection.gid,
        "entry_id": entry.gid,
        "content": entry.content,
        "title": entry.title,
        "status": Entry.EntryChoices(entry.status).name,
        "created_at": entry.created_at.replace(microsecond=0).isoformat(),
        "published_at": entry.created_at.replace(microsecond=0).isoformat(),
    }

    return JsonResponse(data=resp, status=201)


def list_entries(
    request,
    collection_id: str,
    starting_after: Optional[str] = None,
    ending_before: Optional[str] = None,
    limit: int = 20,
):
    limit = int(limit) if limit else constants.MAX_PAGINATION_LIMIT
    if limit > constants.MAX_PAGINATION_LIMIT:
        limit = constants.MAX_PAGINATION_LIMIT

    conditions = [
        starting_after is not None,
        ending_before is not None,
    ]

    if all(conditions):
        raise BadPaginationParameter(
            "One of (starting_after, ending_before) must be supplied"
        )

    try:
        collection = Collection.objects.get(gid=collection_id)
    except Collection.DoesNotExist:
        raise ObjectNotFound("collection")

    query = Entry.objects.filter(user_id=request.user.id).order_by("-gid")

    if starting_after is not None:
        query = query.filter(gid__gt=starting_after)

    if ending_before is not None:
        query = query.filter(gid__lt=ending_before)

    records = query[:limit]

    ret_val = []
    for rec in records:
        ret_val.append(
            EntryOut(
                collection_id=collection.gid,
                title=rec.title,
                entry_id=rec.gid,
                content=rec.content,
                status=rec.status,
                created_at=rec.created_at.replace(microsecond=0).isoformat(),
                published=rec.published_at.replace(microsecond=0).isoformat()
                if rec.published_at
                else None,
            )
        )

    response = ListEntriesResponse(
        limit=limit,
        records=ret_val,
    )

    return JsonResponse(data=response.model_dump(), status=200)


@login_required
@require_http_methods(["GET"])
def get_entry(request, entry_id):
    try:
        entry = Entry.objects.get(
            gid=entry_id,
            user_id=request.user.id,
        )
    except Entry.DoesNotExist:
        raise ObjectNotFound("entry")

    try:
        collection = Collection.objects.get(
            id=entry.collection_id,
            user_id=request.user.id,
        )
    except Collection.DoesNotExist:
        raise ObjectNotFound("collection")

    print(f"entry title: {entry.title}")

    resp = EntryOut(
        collection_id=collection.gid,
        entry_id=entry.gid,
        title=entry.title,
        content=entry.content,
        status=entry.status,
        created_at=entry.created_at.replace(microsecond=0).isoformat(),
        published_at=entry.published_at.replace(microsecond=0).isoformat()
        if entry.published_at
        else None,
    )

    return JsonResponse(data=resp.model_dump(), status=200)
