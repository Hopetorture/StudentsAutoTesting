from django.urls import path
from . import views
from .views import EditTaskView

urlpatterns = [
    # move login code into another app?
    path('', views.login_redirect, name='Login redirect'),
    path('task/<int:pk>/', EditTaskView, name='task-detail'),
    path('assigned/', views.student_choose_course, name='assigned'),
    path('code/', views.code_view, name='code_page'),
    path('code/<int:course>', views.code_view, name='code_page'),
    path('code/test', views.test_code, name='test_code'),
    path('about/', views.about, name='code_about'),
    #path('login/', views.login, name='login_page'),
    path('results/', views.results_view, name='result_table'),
    # result_table_view
]
