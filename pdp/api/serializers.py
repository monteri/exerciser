from enum import Enum
from typing import ForwardRef, List, Optional

from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class CircleStatus(str, Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class CircleIn(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    status: CircleStatus


CircleOut_Partial = ForwardRef("CircleOut")


class CircleOut(CircleIn):
    id: int
    user_id: int
    depth: Optional[int]
    children: Optional[List[CircleOut_Partial]] = []


# Update the forward reference to use the actual CircleOut
CircleOut.update_forward_refs()


class LoginInput(BaseModel):
    username: str
    password: str


class RefreshInput(BaseModel):
    refresh: str


class CircleWithUserOut(BaseModel):
    circle: CircleOut
    user: UserOut


class FullTextSearchResult(BaseModel):
    users: List[UserOut]
    circles: List[CircleOut]
