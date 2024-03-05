import json
import logging
from typing import Optional

import constants
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from exc import (
    BadPaginationParameter,
    ConflictingCollectionName,
    InvalidCollectionTemplate,
    ObjectNotFound,
)
from helpers import generate_id
from journal.models import Collection
from journal.schema import CollectionOut, CollectionTemplate, ListCollectionResponse

logger = logging.getLogger("module::journal")


@login_required
@require_http_methods(["GET", "POST"])
def collections_dispatcher(request, *args, **kwargs):
    if request.method.upper() == "GET":
        params = {
            k: request.GET.get(k, None)
            for k in ["limit", "starting_after", "ending_before", "status"]
        }
        return list_collections(request, **params)

    if request.method.upper() == "POST":
        return create_collection(request, *args, **kwargs)


@login_required
@require_http_methods(["POST"])
def create_collection(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        logger.error("error decoding json body")
        return JsonResponse(data={"detail": "improper data"}, status=400)

    try:
        collection_template = CollectionTemplate(**body["template"])
    except:
        raise InvalidCollectionTemplate()

    existing_collection = None
    try:
        existing_collection = Collection.objects.get(
            user_id=request.user.id,
            name=body["name"],
        )
    except Collection.DoesNotExist:
        logger.info(f"no collections exist for name: {body['name']}")

    if existing_collection is not None:
        raise ConflictingCollectionName(body["name"])

    collection = Collection(
        user_id=request.user.id,
        gid=generate_id(prefix=constants.COLLECTIONS_PREFIX),
        name=body["name"],
        template=collection_template.model_dump(),
        active=body["active"],
        published_entries_count=0,
    )

    collection.save()

    resp = {
        "collection_id": collection.gid,
        "name": collection.name,
        "template": collection.template,
        "active": collection.active,
        "created_at": collection.created_at.replace(microsecond=0).isoformat(),
    }

    return JsonResponse(data=resp, status=201)


@login_required
@require_http_methods(["GET"])
def get_collection(request, collection_id):
    try:
        collection = Collection.objects.get(
            user_id=request.user.id,
            gid=collection_id,
        )
    except Collection.DoesNotExist:
        raise ObjectNotFound("collection")

    resp = {
        "collection_id": collection.gid,
        "name": collection.name,
        "template": collection.template,
        "active": collection.active,
        "created_at": collection.created_at.replace(microsecond=0).isoformat(),
    }

    return JsonResponse(data=resp, status=200)


@login_required
@require_http_methods(["GET"])
def list_collections(
    request,
    starting_after: Optional[str] = None,
    ending_before: Optional[str] = None,
    limit: int = 20,
    status: int = None,
) -> ListCollectionResponse:
    # for now, the list api will just accept the limit and next_cursor parameters
    limit = int(limit)
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

    query = Collection.objects.filter(user_id=request.user.id).order_by("-gid")

    if starting_after is not None:
        query = query.filter(gid__gt=starting_after)

    if ending_before is not None:
        query = query.filter(gid__lt=ending_before)

    # the response will be a list of collections of the given size (provided the list is less than 1MB in size)
    records = query[:limit]

    ret_val = []
    for rec in records:
        ret_val.append(
            CollectionOut(
                collection_id=rec.gid,
                name=rec.name,
                template=rec.template,
                active=rec.active,
                created_at=rec.created_at.replace(microsecond=0).isoformat(),
            )
        )

    response = ListCollectionResponse(
        limit=limit,
        records=ret_val,
    )

    return JsonResponse(data=response.model_dump(), status=200)


def patch(request):
    pass
