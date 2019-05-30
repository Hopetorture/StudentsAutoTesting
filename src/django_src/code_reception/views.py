import json
import logging
import sys

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView

from users.models import StudentGroup, User
from .default_values import SUPPORTED_TOOLSETS
from .models import Task, Course, TaskResult

sys.path.append('..')
from test_engine.judge import judge


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


def code_testing_get_context(request, course, student):
    context = {}
    ctx = list()
    if not student:
        user = request.user
    else:
        user = student
    # Course.objects.get(id=course).task_pool_set
    tasks = user.task_set.filter(course=Course.objects.get(id=course)).all()
    logging.critical(tasks)
    #for e in list(request.user.task_set.all()):
    for e in list(tasks):
        try:
            task_result = e.taskresult_set.get(user=user)
        except ObjectDoesNotExist:
            task_result = TaskResult(test=e, user=user)
            task_result.save()

        logging.info(json.loads(task_result.tests_success))
        task_result.tests_success = json.loads(task_result.tests_success)  # hack, fix later
        ctx.append({'test': e, 'result': task_result})
    context['tasks'] = ctx
    context['course'] = course
    return context


def correct_next_link(next):
    if not next.endswith('/'):
        next += '/'
    if not next.startswith('/'):
        next = '/' + next
    return next


@login_required
def student_choose_course(request, next='/code/'):
    #request.user.course_set
    courses = Course.objects.filter(users=request.user)
    context = {'courses': list(courses),
               'next_link': correct_next_link(next)}
    return render(request, 'code_reception/assigned.html', context)


@login_required
def all_choose_course(request, next='/results/'):
    print('next:', next)
    #request.user.course_set
    courses = Course.objects.all()
    context = {'courses': list(courses),
               'next_link': correct_next_link(next)}
    return render(request, 'code_reception/assigned.html', context)

@login_required
def code_view(request, course=None, student_id=None):
    print('student id:', student_id)
    if not course:
        try:
            course = Course.objects.filter(users=request.user).first().id
        except Exception as e:
            if request.user.groups.filter(name='Teacher').exists():
                redirect('/get_course/')
            # todo - fix issue here when use is fresh and got no courses
            raise e

    if student_id:
        user = User.objects.all().get(id=student_id)
    else:
        user = None
    # import pdb;
    # tasks = list(Task.objects.all()) # debug tutorial
    # pdb.set_trace()
    # print(tasks)
    if request.method == 'POST':
        context = code_testing_get_context(request, course, user)
        logging.info(request.POST)  # we can get the code here

        # after this we need to update context with the code to render it again. and with results.
        # 1) form json request for test engine
        # 2) get response
        # 3) update context end return http request
        print(context)
        # return render(request, 'code_reception/code.html', context)
    else:
        context = code_testing_get_context(request, course, user)
        print(context)
        # pdb.set_trace()
    return render(request, 'code_reception/code.html', context)


@login_required
def test_code(request):
    response_data = {}
    if request.method == 'POST':
        post = request.POST
        if 'student_id' in post:
            user = User.objects.all().get(id=post['student_id'])
            if user != request.user:
                logging.critical('Unauthorized test run')
                messages.error(request, f'Недостаточно прав для запуска', extra_tags='danger')
                return HttpResponse(status=403)
        else:
            user = request.user

        logging.info(post)  # code, lang, task_num
        question_id = post['task']
        task = list(user.task_set.all())[int(question_id) - 1]  # django task object
        logging.critical('Task name being tested:', task.title)
        # if request.user not in task.user_set.all():
        #     logging.critical('Unauthorized test run')
        #     messages.fail(request, f'Недостаточно прав для запуска', extra_tags='danger')
        #     return HttpResponse(status=403)

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
    return HttpResponse(status=404)


def about(request):
    print('about view')
    return render(request, 'code_reception/about.html', {'toolsets': SUPPORTED_TOOLSETS})


def login(request):
    return HttpResponse('<h1>Login page</h1>')


@login_required
def results_view(request, pk):
    context = {'groups': list(StudentGroup.objects.all()),
               'course_id': pk,
               'course_name': Course.objects.get(id=pk).name}

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
        result.save()

    result.submitted_code = code
    result.tests_success = json.dumps([str(case_passed['bool_stat']) for case_passed in results['testcase_status']])
    result.solve_status = results['status']
    result.status_color = results['color']
    result.save()


@login_required
def generate_table(request):
    group = request.POST['group']
    course = Course.objects.get(id=request.POST['course'])
    if request.POST.get('single_student', None):
        students = [StudentGroup.objects.all().get(group_name=group).students.get(id=request.POST.get('single_student'))]
    else:
        students = StudentGroup.objects.all().get(group_name=group).students.all().order_by('last_name', 'first_name')
    response = []
    max_tasks = 0
    for i, student in enumerate(students):
        student_tasks = student.task_set.all().filter(course=course)
        # student_tasks.first().taskresult_set.all().filter(user=student)
        student_results = []
        for task in student_tasks:
            try:
                student_results.append(task.taskresult_set.all().filter(user=student).first().solve_status)
            except AttributeError:
                runstatus = TaskResult(test_id=task.id, user_id=student.id)
                runstatus.save()
                student_results.append(runstatus.solve_status)

        # student_results = [res.solve_status for res in student.taskresult_set.all()]
        if max_tasks < len(student_tasks):
            max_tasks = len(student_tasks)
        progress_str = []
        response.append({
            'name': ' '.join([student.last_name, student.first_name]),
            'email': student.email,
            'idx':  i + 1,
            'results': student_results,
            'db_user_id': student.id,
            'course_id': course.id,
            'progress': 0
        })
    #max_task_num =
    context = {"table": response, 'rows': max_tasks}
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def remove_student_from_group(request, student_id, group_name):
    try:
        print('removed url hit')
        print(student_id, group_name)
        student_obj = User.objects.all().get(pk=student_id)
        StudentGroup.objects.all().get(group_name=group_name).students.remove(student_obj)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)

@login_required
def student_results(request, course):
    course_obj = Course.objects.all().get(id=course)

    return render(request, 'code_reception/student_results.html',
                  {'course': course_obj.name,
                   'course_id': course,
                   'student_group': StudentGroup.objects.all().filter(students=request.user).first(),
                   'student': request.user.id
                   })
