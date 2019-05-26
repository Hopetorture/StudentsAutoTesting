from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from code_reception.models import Course, Task, CoursesCollection
from users.models import StudentGroup

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        #task_choices = forms.MultipleChoiceField(choices=Task.objects.all(), widget=forms.CheckboxSelectMultiple)
        fields = ('assigned_groups', 'tasks_pool', 'name', 'questions_per_student')
        labels = {
            'assigned_groups': 'Добавить новый курс к группам',
            'tasks_pool': 'Выберите задания, которые будут входить в курс',
            'name': 'Имя курса', 'questions_per_student': 'Задач для каждого студента'
        }
        widgets = {
            'tasks_pool': forms.CheckboxSelectMultiple(),
            'assigned_groups': forms.CheckboxSelectMultiple()
        }


class CourseManagment(forms.ModelForm):
    my_field = forms.ModelMultipleChoiceField(queryset=StudentGroup.objects.all(),
                                              widget=FilteredSelectMultiple("StudentGroup",
                                                                            is_stacked=False),
                                              required=False)
    # class Media:
    #     css = {
    #         'all': ('admin/css/widgets.css',)
    #     }
        # js = ('/admin/jsi18n', 'jquery.js', 'jquery.init.js', 'core.js', 'SelectBox.js', 'SelectFilter2.js'),

    class Meta:
        model = Course
        fields = fields = ('assigned_groups', 'tasks_pool', 'name', 'questions_per_student')
        # def __init__(self, *args, **kwargs):
        #     super(CourseManagment, self).__init__(*args, **kwargs)
        #     self.fields['assigned_groups'] = forms.ModelMultipleChoiceField(queryset=StudentGroup.objects.all(), widget=FilteredSelectMultiple('assigned_group', is_stacked=False))
        # widgets = {
        #     'tasks_pool': FilteredSelectMultiple(verbose_name='tasks_pool', is_stacked=False),
        #     'assigned_groups': FilteredSelectMultiple(verbose_name='assigned_groups', is_stacked=False),
        # }

class Try2Form(forms.Form):
    some_name = forms.CharField(max_length=100)
    groups = forms.ModelMultipleChoiceField(queryset=StudentGroup.objects.all(),
                                            widget=FilteredSelectMultiple("Groups", is_stacked=False))
    class Media:
        #css = {'all': ('/static/admin/css/widgets.css',), }
        css = {'all': ('/static/admin/css/responsive.css', '/static/admin/css/widgets.css',
                       # '/static/admin/css/autocomplete.css', '/static/admin/css/base.css',
                       # '/static/admin/css/fonts.css', '/static/admin/css/forms.css',
                       ), }
        js = ('/admin/jsi18n',)


class TaskCreateForm(forms.Form):
    title = forms.CharField(label='Название задачи', required=True,)
    text = forms.CharField(label='Описание задачи', required=True, widget=forms.Textarea)


class CreateTaskModelForm(forms.ModelForm):
    class Meta:
        model = CoursesCollection  # course_set
        fields = ('courses',)
        labels = {
            'courses': 'Добавить к курсам'
        }
        widgets = {
            'courses': forms.SelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(CreateTaskModelForm,  self).__init__(*args, **kwargs)
        self.fields['courses'].required = False


