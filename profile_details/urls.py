from django.urls import path
from profile_details import views
from django.conf.urls import url, include


urlpatterns = [
    path('candidate_profile_add/', views.CandidateProfileAddView.as_view()),
]