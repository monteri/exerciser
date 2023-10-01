from enum import Enum
from typing import Optional


class CircleStatus(str, Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class CircleIn:
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    status: CircleStatus


class CircleOut(CircleIn):
    id: int


class LoginInput:
    username: str
    password: str
