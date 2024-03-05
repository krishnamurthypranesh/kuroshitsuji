from datetime import datetime
from enum import Enum
from typing import List, Optional

from exc import InvalidEnumException
from pydantic import BaseModel, field_serializer


class CustomEnum(Enum):
    def __init__(self, id):
        self._id = id

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls.get_by_name(value)
        return None

    @property
    def id(self):
        return self._id

    @classmethod
    def get_by_id(cls, id):
        for v in cls.__members__.values():
            if v.id == id:
                return v
        raise InvalidEnumException(cls.__name__, id)

    @classmethod
    def get_by_name(cls, name: str):
        if not isinstance(name, str):
            raise InvalidEnumException(cls.__name__, name)

        namel = name.lower()
        for v in cls.__members__.values():
            if v.name.lower() == namel:
                return v
        raise InvalidEnumException(cls.__name__, name)


class CustomBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class CollectionTemplateField(CustomBase):
    key: str
    display_name: str
    required: Optional[bool] = False


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


class EntryStatus(CustomEnum):
    INIT: int = 0
    DRAFT: int = 10
    PUBLISHED: int = 20
    INACTIVE: int = 30


class EntryOut(CustomBase):
    collection_id: str
    entry_id: str
    title: Optional[str] = ""
    content: dict
    status: EntryStatus
    created_at: datetime
    published_at: Optional[datetime] = None

    @field_serializer("status")
    def ser_status(status):
        return status.name


class ListEntriesResponse(CustomBase):
    starting_after: Optional[str] = None
    ending_before: Optional[str] = None
    limit: int
    records: List[EntryOut]
