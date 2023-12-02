from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, FutureDate


class CustomBase(BaseModel):
    pass


class CollectionTemplateField(CustomBase):
    key: str
    display_name: str


class CollectionTemplate(CustomBase):
    fields: List[CollectionTemplateField]


class CreateCollectionRequest(CustomBase):
    name: str
    template: CollectionTemplate
    active: bool = True


class CreateCollectionResponse(CustomBase):
    collection_id: str
    name: str
    template: CollectionTemplate
    active: bool
    created_at: datetime


class CollectionOut(CustomBase):
    collection_id: str
    name: str
    template: CollectionTemplate
    active: bool
    created_at: datetime


class ListCollectionResponse(CustomBase):
    starting_after: Optional[str] = None
    ending_before: Optional[str] = None
    limit: int
    records: List[CollectionOut]
