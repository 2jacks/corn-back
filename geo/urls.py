from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('<slug:username>/fields', views.FieldList.as_view()),
    path('<slug:username>/fields/<int:fieldId>', views.FieldDetail.as_view()),

    path('<slug:username>/fields/<int:fieldId>/researches', views.ResearchList.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>', views.ResearchDetail.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>/files/<slug:filefield>', views.ResearchFiles.as_view()),
    path('<slug:username>/fields/<int:fieldId>/researches/<int:researchId>/aoi', views.ResearchAOIs.as_view()),

]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json',])
