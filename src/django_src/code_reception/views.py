import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import Task

import sys

sys.path.append('..')
from test_engine.judge import judge

# Create your views here.
SUPPORTED_TOOLSETS = [
    {'name': 'c++98', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++98'},
    {'name': 'c++14', 'cmd': 'g++ main.cpp -Wall -fpermissive -std=c++14'},
]


def get_context(request):
    context = {
        # 'tasks': tasks
        # 'tasks': list(Task.objects.all())
        'tasks': list(request.user.task_set.all())
    }
    # context['tasks']['test_success'] = json.loads(context['tasks']['test_success'])
    for e in context['tasks']:
        print(json.loads(e.tests_success))
        e.tests_success = json.loads(e.tests_success)  # hack, fix later
    return context


@login_required
def code_view(request):
    # import pdb;
    # tasks = list(Task.objects.all())
    # pdb.set_trace()
    # print(tasks)
    context = get_context(request)
    if request.method == 'POST':
        context = get_context(request)
        print('Posted')
        print(request.POST)  # we can get the code here

        # after this we need to update context with the code to render it again. and with results.
        # 1) form json request for test engine
        # 2) get response
        # 3) update context end return http request
        return render(request, 'code_reception/code.html', context)
    else:
        context = get_context(request)
        # pdb.set_trace()
        return render(request, 'code_reception/code.html', context)


@login_required
def test_code(request):
    response_data = {}
    if request.method == 'POST':
        # context = get_context(request)

        post = request.POST
        print(post)  # code, lang, task_num
        question_id = post['task']
        task = list(request.user.task_set.all())[int(question_id) - 1] # django task object
        #task.code = post['code']
        code_json = {
            'Type': 'CodeQuestion',
            'Code': post['code'],
            #"JobID": "9",
            "UserID": request.user.id,
            #"QuestionID": task.Question_id,
            "Toolkit": post['lang']
        }

        question_json = task.to_question_json()
        print(task.to_question_json())
        result = judge(task_json=code_json, question=question_json)
        response_data['result'] = result
        update_task_status(task, result)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def about(request):
    print('about view')
    return render(request, 'code_reception/about.html', {'toolsets': SUPPORTED_TOOLSETS})


def login(request):
    return HttpResponse('<h1>Login page</h1>')


@login_required
def results_view(request):
    return render(request, 'code_reception/results.html')


class EditTaskView(DetailView):
    model = Task
    # code_reception/Task_detail.html


def login_redirect(request):
    return redirect('/code/')

# return {
#             'compile_result': compile_result,
#             'testcase_status': [],
#             'status': 'Success'
#         }


def update_task_status(task, results):
    task.tests_success = json.dumps([str(case_passed['bool_stat']) for case_passed in results['testcase_status']])
    task.solve_status = results['status']
    task.status_color = results['color']
    task.save()


