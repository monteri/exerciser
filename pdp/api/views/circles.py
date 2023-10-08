from typing import List

from ninja import Router

from pdp.api.serializers import CircleIn, CircleOut
from pdp.api.utils.security import auth
from pdp.models import Circle

circles_router = Router()


@circles_router.get("/", response=List[CircleOut], auth=auth)
def list_circles(request):
    qs = Circle.objects.all()
    return [
        CircleOut(
            id=c.id,
            name=c.name,
            description=c.description,
            parent_id=c.parent_id,
            status=c.status,
            user_id=request.auth["user_id"],
        )
        for c in qs
    ]


@circles_router.post("/", response={201: CircleOut}, auth=auth)
def create_circle(request, circle_in: CircleIn):
    circle = Circle.objects.create(
        name=circle_in.name,
        description=circle_in.description,
        parent_id=circle_in.parent_id,
        status=circle_in.status,
        user_id=request.auth["user_id"],
    )
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
        user_id=request.auth["user_id"],
    )


@circles_router.get("/{circle_id}/", response=CircleOut, auth=auth)
def retrieve_circle(request, circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
        user_id=request.auth["user_id"],
    )


@circles_router.put("/{circle_id}/", response=CircleOut, auth=auth)
def update_circle(request, circle_id: int, circle_in: CircleIn):
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
        user_id=request.auth["user_id"],
    )


@circles_router.delete("/{circle_id}/", auth=auth)
def delete_circle(request, circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    circle.delete()
    return {"success": True}
