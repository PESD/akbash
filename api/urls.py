from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(
        r'^$',
        views.api_root
    ),
    url(
        r'^employee/$',
        views.EmployeeList.as_view(),
        name="employee-list"
    ),
    url(
        r'^employee/(?P<pk>[0-9]+)/$',
        views.EmployeeDetail.as_view(),
        name="employee-detail"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
