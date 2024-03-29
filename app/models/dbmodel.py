from datetime import datetime
from typing import Optional, Any, Union

from bson import ObjectId
from pydantic import BaseModel, Field, BaseConfig
from pydantic_core import core_schema


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DBModelMixin(DateTimeModelMixin):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    id: str | None = None
