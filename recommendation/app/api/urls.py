from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, UserViewSet

app_name = 'app'
rec_router = path('recommendations/<str:user>/', RecommendationViewSet.as_view(), name = 'recommendations')
user_router = path('users/<str:product>/', UserViewSet.as_view(), name = 'users')
urlpatterns = [
    rec_router,
    user_router,
]
