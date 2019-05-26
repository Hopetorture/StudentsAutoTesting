from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog
from . import views
from code_reception.views import all_choose_course

urlpatterns = [
    path('create_course/', views.create_course, name='create_course'),
    path('create_task/', views.create_task, name='create_task'),
    path('controls/<int:course>/', views.course_controls, name='course_controls'),
    re_path(r'^admin/jsi18n/$', JavaScriptCatalog().get_catalog),
    # path('get_course/controls/', views.course_controls, name='course_controls'),
    # path('get_course/', all_choose_course, name='all_courses_view'),
]