from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'process', views.ProcessViewSet, 'process')
router.register(r'process-by-category/(?P<category_slug>[\w\-.]+)', views.ProcessByCategoryViewSet, 'process-by-category')
router.register(r'activity', views.ActivityViewSet, 'activity')
router.register(r'child-activity', views.ChildActivityViewSet, 'child-activity')
router.register(r'wwa', views.WorkflowWithActivityViewSet, 'wwa')
router.register(r'user', views.UserViewSet)
router.register(r'user-from-username/(?P<username>[\w\-.]+)', views.UserFromUsernameViewSet, "user-from-username")
router.register(r'workflow', views.WorkflowViewSet)
router.register(r'workflow-complete', views.WorkflowCompleteViewSet, "workflow-complete")
router.register(r'workflowactivity', views.WorkflowActivityViewSet, "workflowactivity")
router.register(r'workflowactivity-active-workflow/(?P<workflow_id>[0-9]+)', views.WorkflowActivityFromActiveWorkflowViewSet, "workflowactivity-active-workflow")
router.register(r'workflowactivity-active-user/(?P<user_id>[0-9]+)', views.WorkflowActivityActiveUserViewSet, "workflowactivity-active-user")
router.register(r'workflow-complete-active-user/(?P<username>[\w\-.]+)', views.WorkflowCompleteFromActiveUserViewSet, "workflow-complete-active-user")
router.register(r'workflow-complete-active', views.WorkflowCompleteActiveViewSet, "workflow-complete-active")
router.register(r'workflow-complete-canceled', views.WorkflowCompleteCanceledViewSet, "workflow-complete-canceled")
router.register(r'workflow-complete-completed', views.WorkflowCompleteCompletedViewSet, "workflow-complete-completed")
router.register(r'workflow-from-workflowactivity/(?P<workflowactivity_id>[0-9]+)', views.WorkflowFromWorkflowActivityViewSet, "workflow-from-workflowactivity")
router.register(r'workflow-from-person/(?P<person_id>[0-9]+)', views.WorkflowFromPersonViewSet, "workflow-from-person")
router.register(r'task', views.TaskViewSet)
router.register(r'workflowtask', views.WorkflowTaskViewSet, 'workflowtask')
router.register(r'epar', views.EparViewSet, base_name='epar')
router.register(r'visions-employee', views.VisionsEmployeeViewSet, base_name='visions-employee')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create_workflow/$', views.create_workflow_view),
    url(r'^task_set_epar_id/$', views.task_set_epar_id_view),
    url(r'^task_set_visions_id/$', views.task_set_visions_id_view),
    url(r'^task_check_employee_ad/$', views.task_check_employee_ad_view),
    url(r'^task_check_employee_synergy/$', views.task_check_employee_synergy_view),
    url(r'^task_update_position/$', views.task_update_position_view),
    url(r'^task_generic_check/$', views.task_generic_check_view),
    url(r'^task_generic_todo/$', views.task_generic_todo_view),
    url(r'^task_work_locations/$', views.task_work_locations_view),
]
