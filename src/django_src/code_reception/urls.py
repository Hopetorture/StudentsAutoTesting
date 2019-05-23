from django.urls import path
from . import views
from .views import EditTaskView

urlpatterns = [
    # move login code into another app?
    path('', views.login_redirect, name='Login redirect'),
    path('task/<int:pk>/', EditTaskView, name='task-detail'),
    path('assigned/', views.student_choose_course, name='assigned'),
    path('assigned/<str:next>/', views.student_choose_course, name='assigned_parametrized'),
    path('code/', views.code_view, name='code_page'),
    path('code/<int:course>', views.code_view, name='code_page'),
    path('code/<int:course>/<int:student_id>', views.code_view, name='specific_code_page'),
    path('code/test', views.test_code, name='test_code'),
    path('test/', views.test_code, name='test_code'),
    path('about/', views.about, name='code_about'),
    #path('login/', views.login, name='login_page'),
    path('get_course/', views.all_choose_course, name='all_courses_view'),
    path('get_course/<str:next>/', views.all_choose_course, name='all_courses_view_parametrized'),
    path('results/<int:pk>', views.results_view, name='result_table'),
    path('results/generate_table', views.generate_table, name='generate_table'),
    path('generate_table/', views.generate_table, name='generate_table_crutch'), ###
    path('student_results/<int:course>/', views.student_results, name='student_results'),
    path('results/remove_student_from_group/<int:student_id>/<str:group_name>', views.remove_student_from_group, name='rm_student')
    # result_table_view
]
# remove_student_from_group(request, student_id, group_name)