import json
import random

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CourseCreateForm, TaskCreateForm, CreateTaskModelForm, CourseManagmentForm, CourseManagment
from code_reception.models import Course, Task, TestCase
from users.models import StudentGroup

# Create your views here.

@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            try:
                if Course.objects.all().filter(name=course.name):
                    messages.error(request, f'Такой курс уже существует', extra_tags='danger')

                # add logic to assign students to this course through group
                else:
                    course.save()
                    for student_group in form.cleaned_data['assigned_groups']:
                        course.users.add(*student_group.students.all())
                    course.save()
                    messages.success(request, f'Курс успешно создан')
                    form = CourseCreateForm()
            except Exception as e:
                print(e)
                messages.error(request, f'Ошибка создания', extra_tags='danger')
        else:
            messages.error(request, f'Неправильно заполнена форма', extra_tags='danger')
            # return redirect('profile') todo: DO REDIRECT LATER
    else:
        form = CourseCreateForm()
        #form.fields['Название курса'] = form.fields.pop('name')
        #form.fields['tasks_select'] = form.fields.pop('tasks_pool')
    return render(request, 'teacher_controls/create_course.html', {'form': form})


def check_testcases_valid(testcases):
    for id, case in testcases.items():
        if not case['input'] or not case['output']:
            return False
    return True


def add_testcases_to_task(testcases, task):
    for tc_id, testcase in testcases.items():
        if testcase['testcase_type'] == 'Эталонные значения':
            new_test = TestCase(stdin=testcase['input'],
                                correct_answer=testcase['output'],
                                task=task)
            new_test.save()
            task.testcase_set.add(new_test)



@login_required
def assign_tasks(request):
    print('assign url hit')
    if request.method == 'POST':
        args = request.POST
        course_name = args['Name']
        brackets = int(args['Brackets'])
        assign_to = list(map(int, json.loads(args['Groups'])))
        tasks_by_bracket = {k: list(map(int,v)) for k, v in json.loads(args['Brackets_vals']).items()}
        course_id = int(args['Course_id'])

        course = Course.objects.all().get(id=course_id)
        groups = StudentGroup.objects.all().filter(pk__in=assign_to)

        for group in groups:
            students = group.students.all()
            course.users.add(*students)
            for stud in students:
                already_assigned = stud.task_set.all().filter(course=course)
                if len(already_assigned) != brackets:
                    stud.task_set.remove(*already_assigned)
                    for bracket_id, tasks in tasks_by_bracket.items():
                        if not tasks:
                            break
                        task = Task.objects.all().get(pk=random.choice(tasks))
                        stud.task_set.add(task)
                # for bracket in brackets:
                #     task = bracket.get_random.task()
                #     stud.task_set.add(task)


        return HttpResponse(status=200)

    else:
        return HttpResponse(status=500)

@login_required
def create_task(request):
    courses_form = CreateTaskModelForm()
    if request.method == 'POST':
        print(request.POST)  #  add_to_courses_[]
        print(request.POST.get('add_to_courses_'))
        print('post')
        form = TaskCreateForm(request.POST)
        test_cases = json.loads(request.POST.get('tests_', '{}'))
        title = request.POST.get('title_data')
        description = request.POST.get('description_data')
        print(test_cases)
        if (test_cases and title and description and check_testcases_valid(test_cases)):
            new_task = Task(title=title, text=description)
            new_task.save()
            add_testcases_to_task(test_cases, new_task)
            print('valid forms')
            messages.success(request, 'Задача успешно создана')
        else:
            print('not valid forms')
            messages.error(request, 'Необходимо заполнить все обязательные поля', extra_tags='danger')
        return render(request, 'teacher_controls/create_task.html', {'form': form, 'courses_form': courses_form})

    else:
        print('task')
        form = TaskCreateForm()

        #return HttpResponse()
    return render(request, 'teacher_controls/create_task.html', {'form': form, 'courses_form': courses_form})

@login_required
def course_controls(request, course=None):
    course_obj = Course.objects.all().get(id=course)
    if request.method == 'POST':
        try:
            course_obj.name = request.POST['Name']
            course_obj.questions_per_student = int(request.POST['Brackets'])
            course_obj.tasks_pool.set(Task.objects.all().filter(pk__in=map(int, json.loads(request.POST['Task_pool']))))
            course_obj.assigned_groups.set(StudentGroup.objects.all().filter(pk__in=map(int, json.loads(request.POST['Groups']))))

            brackets = json.loads(request.POST['Brackets_vals'])
            for idx, vals in brackets.items():
                if not vals:
                    break
                # br = getattr(course_obj, 'bracket_{}'.format(idx))
                br = Task.objects.all().filter(id__in=map(int, vals))
                # setattr(course_obj, 'bracket_{}'.format(idx), br)
                field = 'bracket_{}'.format(idx)
                eval('course_obj.{}.set(br)'.format(field))

            course_obj.save()
        except:
            messages.error(request, 'Произошла ошибка', extra_tags='danger')
            return HttpResponse(status=500)
            pass # Report error

        form = CourseManagment(instance=course_obj, course_id=course)
        print('message added')
        messages.success(request, 'Курс успешно изменен')
        return render(request, 'teacher_controls/course_controls.html',
                      {'course_name': course_obj.name, 'form': form})
        # form = CourseManagment(request.POST, course_id=course)
        # if form.is_valid():
        #     course = form.save(commit=False)
        #     course.save()
        #     messages.success(request, 'Курс успешно изменен')

        # else:
        #     messages.error(request, 'Форма неправильно заполнена', extra_tags='danger')
        #     #print(form.errors)

        # return render(request, 'teacher_controls/course_controls.html',
        #               {'course_name': course_obj.name, 'form': form})


    else:
        print('URL HIT!')
        #form = CourseManagmentForm()
        form = CourseManagment(instance=course_obj, course_id=course)
        return render(request, 'teacher_controls/course_controls.html', {'course_name': course_obj.name, 'form': form})
