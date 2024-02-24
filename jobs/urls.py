from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.jobs, name='jobs'),
    path('create-job/', views.createJob, name='createJob'),
    path('saved/', views.saved, name='saved'),
    
]