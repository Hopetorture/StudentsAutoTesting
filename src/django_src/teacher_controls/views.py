import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CourseCreateForm, TaskCreateForm, CreateTaskModelForm
from code_reception.models import Course

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


@login_required
def create_task(request):
    if request.method == 'POST':
        print(request.POST)
        print('post')
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        print('task')
        form = TaskCreateForm()
        courses_form = CreateTaskModelForm()
        #return HttpResponse()
    return render(request, 'teacher_controls/create_task.html', {'form': form, 'courses_form': courses_form})