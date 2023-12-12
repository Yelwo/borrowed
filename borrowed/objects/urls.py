from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'objects', views.ObjectViewSet, basename='objects')
router.register(r'borrows', views.BorrowViewSet, basename='borrows')



urlpatterns = [
    path('', include(router.urls)),
    path('borrows/lent/', views.BorrowViewSet.as_view({"list": "lent"})),
    path('borrows/borrowed/', views.BorrowViewSet.as_view({"list": "borrowed"})),
    path('borrows/borrowed/<int:pk>/return/', views.BorrowViewSet.as_view({"update": "return_borrowed_object"})),
]