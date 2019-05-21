from django.urls import path

from . import views

urlpatterns = [
    path('create_course/', views.create_course, name='create_course'),
    path('create_task/', views.create_task, name='create_task'),
]