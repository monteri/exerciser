from typing import List

from ninja import Router

from pdp.api.serializers import CircleIn, CircleOut
from pdp.api.utils.security import auth
from pdp.models import Circle

circles_router = Router()


@circles_router.get("/circles/", response=List[CircleOut], auth=auth)
def list_circles():
    qs = Circle.objects.all()
    return [
        CircleOut(
            id=c.id,
            name=c.name,
            description=c.description,
            parent_id=c.parent_id,
            status=c.status,
        )
        for c in qs
    ]


@circles_router.post("/circles/", response=CircleOut, auth=auth)
def create_circle(circle_in: CircleIn):
    circle = Circle.objects.create(
        name=circle_in.name,
        description=circle_in.description,
        parent_id=circle_in.parent_id,
        status=circle_in.status
        # Add user assignment if needed
    )
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
    )


@circles_router.get("/circles/{circle_id}/", response=CircleOut, auth=auth)
def retrieve_circle(circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
    )


@circles_router.put("/circles/{circle_id}/", response=CircleOut, auth=auth)
def update_circle(circle_id: int, circle_in: CircleIn):
    circle = Circle.objects.get(id=circle_id)
    for field in ["name", "description", "parent_id", "status"]:
        setattr(circle, field, getattr(circle_in, field))
    circle.save()
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
    )


@circles_router.delete("/circles/{circle_id}/", auth=auth)
def delete_circle(circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    circle.delete()
    return {"success": True}
