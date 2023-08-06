from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.recruitment import views


router = DefaultRouter()
router.register('attributefiltersets', views.AttributeFilterSetViewSet)
router.register('projects', views.ProjectViewSet)
router.register('contacthistories', views.ContactHistoryViewSet, basename='contacthistory')

attributefilterset_router = NestedDefaultRouter(router, 'attributefiltersets',
                                                lookup='attributefilterset')
attributefilterset_router.register('participations', views.ParticipationViewSet,
                                   basename='participation')

project_router = NestedDefaultRouter(router, 'projects', lookup='project')
project_router.register('subjectgroups', views.SubjectGroupViewset, basename='subjectgroup')

urlpatterns = router.urls
urlpatterns += attributefilterset_router.urls
urlpatterns += project_router.urls
