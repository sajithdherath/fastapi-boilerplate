from typing import List, Dict, Any

from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
