from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
SUPPORTED_TOOLSETS = [
    {'name': 'c++98', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++98'},
    {'name': 'c++14', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++14'},
]

tasks =[
    {
        'Question_id': '42',
        'Title': 'Sorting',
        'Text': 'this is a task',
        'Timeout': '3',
        'status': 'fail',
        'status_color': 'red',
        'test_success': ['True', 'True', 'False']
    },
    {
        'Question_id': '43',
        'Title': 'Lookup',
        'Text': 'this is a task 2',
        'Timeout': '4',
        'status': 'success',
        'status_color': 'green',
        'test_success': ['True', 'False', 'False']

    },
    {
        'Question_id': '43',
        'Title': 'Binary trees',
        'Text': 'Ipsum Lorem',
        'Timeout': '4',
        'status': 'no run',
        'status_color': 'black',
        'test_success': []

    }

]

def code_view(request):
    context = {
        'tasks': tasks
    }
    return render(request, 'code_reception/code.html', context)


def about(request):
    return render(request, 'code_reception/about.html', {'toolsets': SUPPORTED_TOOLSETS})


def login(request):
    return HttpResponse('<h1>Login page</h1>')


def results_view(request):
    return HttpResponse('<h1>View students progress table goes here</h1>')


def login_redirect(request):
    return redirect('/login/')

