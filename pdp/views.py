from typing import List

from ninja import NinjaAPI
from .models import Circle
from .serializers import CircleOut, CircleIn

api = NinjaAPI()


@api.get("/circles/", response=List[CircleOut])
def list_circles(request):
    qs = Circle.objects.all()
    return [CircleOut(id=c.id, name=c.name, description=c.description, parent_id=c.parent_id, status=c.status) for c in qs]


@api.post("/circles/", response=CircleOut)
def create_circle(request, circle_in: CircleIn):
    circle = Circle.objects.create(
        name=circle_in.name,
        description=circle_in.description,
        parent_id=circle_in.parent_id,
        status=circle_in.status
        # Add user assignment if needed
    )
    return CircleOut(id=circle.id, name=circle.name, description=circle.description, parent_id=circle.parent_id, status=circle.status)


@api.get("/circles/{circle_id}/", response=CircleOut)
def retrieve_circle(request, circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    return CircleOut(id=circle.id, name=circle.name, description=circle.description, parent_id=circle.parent_id, status=circle.status)


@api.put("/circles/{circle_id}/", response=CircleOut)
def update_circle(request, circle_id: int, circle_in: CircleIn):
    circle = Circle.objects.get(id=circle_id)
    for field in ["name", "description", "parent_id", "status"]:
        setattr(circle, field, getattr(circle_in, field))
    circle.save()
    return CircleOut(id=circle.id, name=circle.name, description=circle.description, parent_id=circle.parent_id, status=circle.status)


@api.delete("/circles/{circle_id}/")
def delete_circle(request, circle_id: int):
    circle = Circle.objects.get(id=circle_id)
    circle.delete()
    return {"success": True}

