from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'modellog', views.ModelLogViewSet, 'modellog')
router.register(r'modellog-by-person/(?P<person_id>[0-9]+)', views.ModelLogByPersonViewSet, "modellog-by-person")

urlpatterns = [
    url(r'^', include(router.urls)),
]
