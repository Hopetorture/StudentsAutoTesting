from django import forms
from code_reception.models import Course, Task

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        #task_choices = forms.MultipleChoiceField(choices=Task.objects.all(), widget=forms.CheckboxSelectMultiple)
        fields = ('assigned_groups', 'tasks_pool', 'name',)
        labels = {
            'assigned_groups': 'Добавить новый курс к группам',
            'tasks_pool': 'Выберите задания, которые будут входить в курс',
            'name': 'Имя курса'
        }
        widgets = {
            'tasks_pool': forms.CheckboxSelectMultiple(),
            'assigned_groups': forms.CheckboxSelectMultiple()
        }

class TaskCreateForm(forms.Form):
    title = forms.CharField(label='Название задачи', required=True,)
    text = forms.CharField(label='Описание задачи', required=True, widget=forms.Textarea)


