import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task


# Create your views here.
SUPPORTED_TOOLSETS = [
    {'name': 'c++98', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++98'},
    {'name': 'c++14', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++14'},
]

# tasks =[
#     {
#         'Question_id': '42',
#         'Title': 'Sorting',
#         'Text': 'this is a task',
#         'Timeout': '3',
#         'status': 'fail',
#         'status_color': 'red',
#         'test_success': ['True', 'True', 'False']
#     },
#     {
#         'Question_id': '43',
#         'Title': 'Lookup',
#         'Text': 'this is a task 2',
#         'Timeout': '4',
#         'status': 'success',
#         'status_color': 'green',
#         'test_success': ['True', 'False', 'False']
#
#     },
#     {
#         'Question_id': '43',
#         'Title': 'Binary trees',
#         'Text': 'Ipsum Lorem',
#         'Timeout': '4',
#         'status': 'no run',
#         'status_color': 'black',
#         'test_success': []
#
#     }
#
# ]

def code_view(request):

    #import pdb;
    # tasks = list(Task.objects.all())
    #pdb.set_trace()
    # print(tasks)
    context = {
        #'tasks': tasks
        'tasks': list(Task.objects.all())
    }
    #context['tasks']['test_success'] = json.loads(context['tasks']['test_success'])
    for e in context['tasks']:
        print(json.loads(e.tests_success))
        e.tests_success = json.loads(e.tests_success)  # hack, fix later
    #pdb.set_trace()
    return render(request, 'code_reception/code.html', context)


def about(request):
    return render(request, 'code_reception/about.html', {'toolsets': SUPPORTED_TOOLSETS})


def login(request):
    return HttpResponse('<h1>Login page</h1>')


def results_view(request):
    return HttpResponse('<h1>View students progress table goes here</h1>')


def login_redirect(request):
    return redirect('/login/')

