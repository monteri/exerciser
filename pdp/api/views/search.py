from django.contrib.auth.models import User
from django.db.models import Q

from ninja import Query, Router

from pdp.api.serializers import CircleOut, FullTextSearchResult, UserOut
from pdp.api.services.security import auth
from pdp.models import Circle

search_router = Router()


@search_router.get("/", response=FullTextSearchResult, auth=auth)
def full_text_search(request, query: str = Query(...)):
    # Perform a full-text search on Circle names and descriptions
    circle_results = Circle.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )

    # Perform a full-text search on User usernames, emails, first names, and last names
    user_results = User.objects.filter(
        Q(username__icontains=query)
        | Q(email__icontains=query)
        | Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
    )

    # Serialize the query results using the respective serializers
    circle_results = [CircleOut(**circle.__dict__) for circle in circle_results]
    user_results = [UserOut(**user.__dict__) for user in user_results]

    return {"users": user_results, "circles": circle_results}
