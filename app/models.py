from pydantic.main import BaseModel


class HealthResponse(BaseModel):
    status: str


class Item(BaseModel):
    _id: str = None
    name: str
