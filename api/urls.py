from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

# Django REST Framework routers
router = DefaultRouter()
router.register(r'employee', views.EmployeeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
