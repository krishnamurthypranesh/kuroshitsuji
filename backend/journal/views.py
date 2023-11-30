import json
import logging

import constants
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from exc import ConflictingCollectionName, InvalidCollectionTemplate
from helpers import generate_id
from journal.models import Collection
from journal.schema import CollectionTemplate

logger = logging.getLogger("module::journal")


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
        "created_at": collection.created_at.isoformat(),
    }

    return JsonResponse(data=resp, status=201)


@login_required
@require_http_methods(["GET"])
def get_collection(request):
    collection = Collection.objects.get(
        user_id=request.user.id,
        gid=request.params["gid"],
    )
    return {
        "collection_id": collection.gid,
        "name": collection.name,
        "template": collection.template,
        "active": collection.active,
        "created_at": collection.created_at.isoformat(),
    }


# def list_items(
#     self,
#     next_cursor: Optional[str] = None,
#     prev_cursor: Optional[str] = None,
#     limit: int = 20,
#     auth_token = Depends(authorize),
# ) -> ListCollectionResponse:
#     # for now, the list api will just accept the limit and next_cursor parameters
#     if limit > constants.MAX_PAGINATION_LIMIT:
#         limit = constants.MAX_PAGINATION_LIMIT

#     conditions = [
#         next_cursor is not None,
#         prev_cursor is not None,
#     ]

#     if all(conditions):
#         raise BadPaginationParameter()

#     scan_forward = True
#     cursor = ""
#     if next_cursor is not None:
#         cursor = next_cursor

#     if prev_cursor is not None:
#         cursor = prev_cursor
#         scan_forward = False

#     # the response will be a list of collections of the given size (provided the list is less than 1MB in size)
#     records, key = self.painted_porch_repo.get_all_collections_by_params(
#         user_id=auth_token.user.user_id,
#         cursor=cursor,
#         scan_forward=scan_forward,
#         limit=limit,
#     )

#     ret_val = []
#     for rec in records:
#         ret_val.append(
#             CollectionOut(
#                 collection_id=rec.collection_id,
#                 name=rec.collection_id,
#                 template=rec.template,
#                 active=rec.active,
#                 created_at=rec.created_at.isoformat(),
#             )
#         )

#     if scan_forward:
#         prev_cursor = next_cursor
#         next_cursor = key
#     else:
#         next_cursor = prev_cursor
#         prev_cursor = key

#     return ListCollectionResponse(
#         next_cursor=next_cursor,
#         prev_cursor=prev_cursor,
#         limit=limit,
#         records=ret_val,
#     )


def patch(request):
    pass
