from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

# Django REST Framework routers
router = DefaultRouter()
router.register(r'employee', views.EmployeeViewSet)
router.register(r'contractor', views.ContractorViewSet)
router.register(r'position', views.PositionViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'department', views.DepartmentViewSet)
router.register(r'position-type', views.PositionTypeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
