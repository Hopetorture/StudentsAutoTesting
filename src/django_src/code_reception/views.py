from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.


def code_view(request):
    return HttpResponse('<h1>Code home</h1>')


def about(request):
    return HttpResponse('<h1>Tools info</h1>')


def login(request):
    return HttpResponse('<h1>Login page</h1>')


def results_view(request):
    return HttpResponse('<h1>View students progress table goes here</h1>')


def login_redirect(request):
    return redirect('/login/')

