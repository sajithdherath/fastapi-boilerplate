from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DBModelMixin(DateTimeModelMixin):
    id: Optional[ObjectId] = Field(alias='_id')
