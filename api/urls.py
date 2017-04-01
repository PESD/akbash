from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^employee/$', views.employee_list),
    url(r'^employee/(?P<pk>[0-9]+)/$', views.employee_detail),
]
