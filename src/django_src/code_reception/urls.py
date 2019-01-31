from django.urls import path
from . import views


urlpatterns = [
    # move login code into another app?
    #path('', views.login_redirect, name='Login redirect'),
    path('code/', views.code_view, name='code_page'),
    path('about/', views.about, name='code_about'),
    #path('login/', views.login, name='login_page'),
    path('results/', views.results_view, name='result_table'),
]
