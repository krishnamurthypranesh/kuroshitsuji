from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, FutureDate


class CustomBase(BaseModel):
    pass


class CustomEnum(BaseModel, Enum):
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


class EntryStatus(Enum):
    INIT: int = 0
    DRAFT: int = 10
    PUBLISHED: int = 20
    INACTIVE: int = 30


class EntryOut(CustomBase):
    collection_id: str
    entry_id: str
    content: dict
    status: EntryStatus
    created_at: datetime
    published: Optional[datetime] = None
