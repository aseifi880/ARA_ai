from django.urls import path
from jobyabi import views

urlpatterns = [
    path('scrape_resumes/', views.JobyabiResumeView.as_view(), name='index'),
]
