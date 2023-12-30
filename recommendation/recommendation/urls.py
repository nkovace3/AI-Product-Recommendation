from django.contrib import admin
from django.urls import path, include
from app.api.urls import rec_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.api.urls')),
    rec_router,
]