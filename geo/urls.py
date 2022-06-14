from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import AnalysisViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('<slug:username>/fields', views.FieldList.as_view()),
    path('<slug:username>/fields/<int:fieldId>', views.FieldDetail.as_view()),

    path('<slug:username>/fields/<int:fieldId>/researches', views.ResearchList.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>', views.ResearchDetail.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>/files/<slug:filefield>',
         views.ResearchFiles.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>/aoi', views.ResearchAOIs.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>/fitoscan', views.FitoScan.as_view()),

]

router = DefaultRouter()
router.register(r'analysis', AnalysisViewSet, basename='analysis')

urlpatterns += router.urls
