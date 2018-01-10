from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

# Django REST Framework routers
router = DefaultRouter()
router.register(r'employee', views.EmployeeViewSet, 'employee')
router.register(r'contractor', views.ContractorViewSet, 'contractor')
router.register(r'vendor', views.VendorViewSet, 'vendor')
router.register(r'position', views.PositionViewSet, 'position')
router.register(r'location', views.LocationViewSet)
router.register(r'location-from-person/(?P<person_id>[0-9]+)', views.LocationFromPerson, "location-from-person")
router.register(r'location-not-from-person/(?P<person_id>[0-9]+)', views.LocationNotFromPerson, "location-not-from-person")
router.register(r'department', views.DepartmentViewSet)
router.register(r'position-type', views.PositionTypeViewSet)
router.register(r'employee-no-workflow', views.EmployeeNoWorkflowViewSet, 'employee-no-workflow')
router.register(r'employee-new-hire-no-workflow', views.EmployeeNewHireNoWorkflowViewSet, 'employee-new-hire-no-workflow')
router.register(r'person', views.PersonViewSet, 'person')
router.register(r'person-missed-start-date', views.PersonMissedStartDateViewSet, 'person-missed-start-date')
router.register(r'person-all-contractors', views.PersonAllContractorsViewSet, 'person-all-contractors')
router.register(r'person-all-employees', views.PersonAllEmployeesViewSet, 'person-all-employees')
router.register(r'person-all-subs', views.PersonAllLongTermSubsViewSet, 'person-all-subs')
router.register(r'person-from-workflow/(?P<workflow_id>[0-9]+)', views.PersonFromWorkflowViewSet, 'person-from-workflow')
router.register(r'position-from-person/(?P<person_id>[0-9]+)', views.PositionFromPersonViewSet, "position-from-person")
router.register(r'comment', views.CommentViewSet)
router.register(r'comment-from-person/(?P<person_id>[0-9]+)', views.CommentFromPersonViewSet, "comment-from-person")
router.register(r'user', views.UserViewSet)
router.register(r'visionspositions', views.VisionsPositionsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
