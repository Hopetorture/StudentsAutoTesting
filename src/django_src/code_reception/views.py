import json
import sys
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist

from .models import Task, Course, TaskResult
from .default_values import SUPPORTED_TOOLSETS
from users.models import StudentGroup, Profile

sys.path.append('..')
from test_engine.judge import judge


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


def get_context(request, course):
    context = {}
    ctx = list()
    # Course.objects.get(id=course).task_pool_set
    tasks = request.user.task_set.filter(course=Course.objects.get(id=course)).all()
    logging.critical(tasks)
    #for e in list(request.user.task_set.all()):
    for e in list(tasks):
        try:
            task_result = e.taskresult_set.get(user=request.user)
        except ObjectDoesNotExist:
            task_result = TaskResult(test=e, user=request.user)
        logging.info(json.loads(task_result.tests_success))
        task_result.tests_success = json.loads(task_result.tests_success)  # hack, fix later
        ctx.append({'test': e, 'result': task_result})
    context['tasks'] = ctx
    context['course'] = course
    return context


@login_required
def student_choose_course(request):
    #request.user.course_set
    courses = Course.objects.filter(users=request.user)
    context = {'courses': list(courses)}
    return render(request, 'code_reception/assigned.html', context)


@login_required
def code_view(request, course=None):
    if not course:
        course = Course.objects.filter(users=request.user).first().id

    # import pdb;
    # tasks = list(Task.objects.all()) # debug tutorial
    # pdb.set_trace()
    # print(tasks)
    if request.method == 'POST':
        context = get_context(request, course)
        logging.info(request.POST)  # we can get the code here

        # after this we need to update context with the code to render it again. and with results.
        # 1) form json request for test engine
        # 2) get response
        # 3) update context end return http request
        return render(request, 'code_reception/code.html', context)
    else:
        context = get_context(request, course)
        # pdb.set_trace()
        return render(request, 'code_reception/code.html', context)


@login_required
def test_code(request):
    response_data = {}
    if request.method == 'POST':
        post = request.POST
        logging.info(post)  # code, lang, task_num
        question_id = post['task']
        task = list(request.user.task_set.all())[int(question_id) - 1]  # django task object

        code_json = {
            'Type': 'CodeQuestion',
            'Code': post['code'],
            #"JobID": "9",
            "UserID": request.user.id,
            #"QuestionID": task.Question_id,
            "Toolkit": post['lang']
        }

        question_json = task.to_question_json()
        logging.info(task.to_question_json())
        result = judge(task_json=code_json, question=question_json)
        response_data['result'] = result
        update_task_status(task, result, post['code'], request.user)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def about(request):
    print('about view')
    return render(request, 'code_reception/about.html', {'toolsets': SUPPORTED_TOOLSETS})


def login(request):
    return HttpResponse('<h1>Login page</h1>')


@login_required
def results_view(request):
    context = {'groups': list(StudentGroup.objects.all())}
    return render(request, 'code_reception/results.html', context)


class EditTaskView(DetailView):
    model = Task
    # code_reception/Task_detail.html


def login_redirect(request):
    return redirect('/code/')


def update_task_status(task, results, code, user):
    #result = task.taskresult_set.get(user=user.profile)
    try:
        result = TaskResult.objects.get(test_id=task.id, user_id=user.id)
    except ObjectDoesNotExist:
    #if not result:
        result = TaskResult(test_id=task.id, user_id=user.id)

    result.submitted_code = code
    result.tests_success = json.dumps([str(case_passed['bool_stat']) for case_passed in results['testcase_status']])
    result.solve_status = results['status']
    result.status_color = results['color']
    result.save()


@login_required
def generate_table(request):
    group = request.POST['group']
    students = StudentGroup.objects.all().get(group_name=group).students.all()
    students = StudentGroup.objects.all().get(group_name=group).students.all().order_by('last_name', 'first_name')
    response = []
    for i, student in enumerate(students):
        response.append({
            'name': ' '.join([student.last_name, student.first_name]),
            'idx':  i + 1,
        })

    return HttpResponse(json.dumps({"table": response}), content_type="application/json")


