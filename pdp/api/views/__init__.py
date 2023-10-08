from ninja import NinjaAPI

from pdp.api.views.auth import auth_router
from pdp.api.views.circles import circles_router
from pdp.api.views.search import search_router

api = NinjaAPI(urls_namespace="api")


api.add_router("auth", auth_router)
api.add_router("circles", circles_router)
api.add_router("search", search_router)
