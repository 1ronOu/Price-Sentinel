from pydantic import BaseModel


class Token(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = 'Bearer'


class TokenData(BaseModel):
    user_id: str | None = None