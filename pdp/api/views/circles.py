from typing import List

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator

from ninja import Query, Router
from ninja.errors import HttpError

from pdp.api.serializers import CircleIn, CircleOut, CircleWithUserOut, UserOut
from pdp.api.services.circle_services import get_circle_with_children
from pdp.api.services.security import auth
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
    # If a parent_id is provided, fetch the parent and check its depth
    if circle_in.parent_id:
        parent_circle = Circle.objects.get(id=circle_in.parent_id)
        if parent_circle.depth >= 5:
            raise HttpError(
                status_code=400, message="Cannot create circle beyond a depth of 5"
            )

        depth = parent_circle.depth + 1
    else:
        depth = 0

    circle = Circle.objects.create(
        name=circle_in.name,
        description=circle_in.description,
        parent_id=circle_in.parent_id,
        status=circle_in.status,
        user_id=request.auth["user_id"],
        depth=depth,
    )
    return CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
        user_id=request.auth["user_id"],
        depth=depth,
    )


@circles_router.get("/{circle_id}/", response=CircleOut, auth=auth)
def retrieve_circle(request, circle_id: int):
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        raise HttpError(
            status_code=404, message=f"ID: {circle_id} is not present in the database."
        )
    return get_circle_with_children(circle)


@circles_router.put("/{circle_id}/", response=CircleOut, auth=auth)
def update_circle(request, circle_id: int, circle_in: CircleIn):
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        raise HttpError(
            status_code=404, message=f"ID: {circle_id} is not present in the database."
        )

    # If changing the parent
    if circle_in.parent_id is not None and circle_in.parent_id != circle.parent_id:
        try:
            parent_circle = Circle.objects.get(id=circle_in.parent_id)
        except Circle.DoesNotExist:
            raise HttpError(
                status_code=404,
                message=f"parent_id={circle_in.parent_id} is"
                f" not present in the database.",
            )

        if parent_circle.depth >= 5:
            raise HttpError(
                status_code=400, message="Cannot move circle beyond a depth of 5"
            )
        circle.depth = parent_circle.depth + 1

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
        depth=circle.depth,
    )


@circles_router.delete("/{circle_id}/", auth=auth)
def delete_circle(request, circle_id: int):
    try:
        circle = Circle.objects.get(id=circle_id)
    except Circle.DoesNotExist:
        raise HttpError(
            status_code=404, message=f"ID: {circle_id} is not present in the database."
        )
    circle.delete()
    return {"success": True}
