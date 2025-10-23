from django.urls import path

from jobyabi import views

urlpatterns = [
    path('scrape_resumes/', views.scrape_jobs, name='index'),
]
