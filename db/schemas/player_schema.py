# stdlib
from datetime import datetime
from typing import Optional

# thirdparty
from pydantic import BaseModel


class PlayerInfoSchema(BaseModel):
    player_id: int


class PlayerSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: Optional[datetime]


class PlayerCreate(BaseModel):
    player_id: int
    username: Optional[str] = None
