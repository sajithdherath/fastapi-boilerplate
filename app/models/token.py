from pydantic import BaseModel


class TokenPayload(BaseModel):
    email: str = ""


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
