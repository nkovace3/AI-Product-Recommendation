from rest_framework.routers import DefaultRouter
from app.api.urls import rec_router
from django.urls import path, include

router = DefaultRouter()
# router.registry.extend(rec_router.registry)

urlpatterns = [
    path('', include(router.urls))
]
