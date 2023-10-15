from typing import List

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator

from ninja import Query, Router

from pdp.api.serializers import CircleIn, CircleOut, CircleWithUserOut, UserOut
from pdp.api.utils.security import auth
from pdp.models import Circle, UserAccount

circles_router = Router()


@circles_router.get("/", response=List[CircleWithUserOut], auth=auth)
def list_circles(request, page_number: int = Query(1, alias="page")):
    cache_key = f"circles_list_{page_number}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    qs = UserAccount.objects.select_related("circle__user").all()
    paginator = Paginator(qs, settings.ACCOUNTS_PER_PAGE)
    page = paginator.get_page(page_number)

    result = []
    for user_account in page:
        if not user_account.circle_id:
            continue
        circle = user_account.circle
        user_data = circle.user
        result.append(
            {
                "circle": CircleOut(
                    id=circle.id,
                    name=circle.name,
                    description=circle.description,
                    parent_id=circle.parent_id,
                    status=circle.status,
                    user_id=user_data.id,
                ),
                "user": UserOut(
                    id=user_data.id,
                    username=user_data.username,
                    email=user_data.email,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                ),
            }
        )

    cache.set(cache_key, result, 15 * 60)

    return result


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
