from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import EmployeeViewSet, upload_photo

router = DefaultRouter()
router.register(r'divisions', views.DivisionViewSet)
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', upload_photo, name='upload_photo'),
]