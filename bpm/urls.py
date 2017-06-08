from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'process', views.ProcessViewSet)
router.register(r'activity', views.ActivityViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'workflow', views.WorkflowViewSet)
router.register(r'workflow-complete', views.WorkflowCompleteViewSet)
router.register(r'workflowactivity', views.WorkflowActivityViewSet)
router.register(r'workflowactivity-active-user/(?P<user_id>[0-9]+)', views.WorkflowActivityActiveUserViewSet, "workflowactivity-active-user")
router.register(r'workflow-complete-active-user/(?P<user_id>[0-9]+)', views.WorkflowCompleteFromActiveUserViewSet, "workflow-complete-active-user")
router.register(r'workflow-complete-active', views.WorkflowCompleteActiveViewSet, "workflow-complete-active")
router.register(r'workflow-from-workflowactivity/(?P<workflowactivity_id>[0-9]+)', views.WorkflowFromWorkflowActivityViewSet, "workflow-from-workflowactivity")
router.register(r'workflow-from-person/(?P<person_id>[0-9]+)', views.WorkflowFromPersonViewSet, "workflow-from-person")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create_workflow/$', views.create_workflow_view),
]
