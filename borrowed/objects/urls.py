from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'objects', views.ObjectViewSet, basename='objects')
router.register(r'borrows', views.BorrowViewSet, basename='borrows')



urlpatterns = [
    path('', include(router.urls)),
]