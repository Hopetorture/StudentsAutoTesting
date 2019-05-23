import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CourseCreateForm, TaskCreateForm, CreateTaskModelForm
from code_reception.models import Course, Task, TestCase

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
    # 1) Разбиение задач на брекеты
    # 2) Cписок задач
    # 3) Добавление задач
    # 4) Кнопка "выдать студентам задачи"
    # 5) возможность изменить задачу?
    print('URL HIT!')
    course_obj = Course.objects.all().get(id=course)
    return render(request, 'teacher_controls/course_controls.html', {'course_name': course_obj.name + str('''# 1) Разбиение задач на брекеты
    # 2) Cписок задач
    # 3) Добавление задач
    # 3.1) Добавить/убрать группу
    # 4) Кнопка "выдать группе задачи"
    # 5) возможность изменить задачу?''')})