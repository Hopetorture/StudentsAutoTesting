from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from code_reception.models import Course, Task, CoursesCollection
from users.models import StudentGroup


BRACKET_LIST = ['bracket_' + str(i) for i in range(1, 31)]
CRUTCH = ['tasks_pool'] + ['assigned_groups'] + BRACKET_LIST

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
    # some_name = forms.CharField(max_length=100)
    # groups = forms.ModelMultipleChoiceField(queryset=StudentGroup.objects.all(),
    #                                         widget=FilteredSelectMultiple("Groups", is_stacked=False))
    #bracket_0 = forms.ModelMultipleChoiceField(queryset=Task.objects.all(),
    #                                        widget=FilteredSelectMultiple("bra 0", is_stacked=False))
    # @property
    # def get_bracket(self):
    #     forms.ModelMultipleChoiceField(queryset=Course.objects.get(id=self.course_id).bracket_1.objects().all(),
    #                                    widget=FilteredSelectMultiple("Bracket_1", is_stacked=False))

    class Media:
        #css = {'all': ('/static/admin/css/widgets.css',), }
        css = {'all': ('/static/admin/css/responsive.css', '/static/admin/css/widgets.css',
                       # '/static/admin/css/autocomplete.css', '/static/admin/css/base.css',
                       # '/static/admin/css/fonts.css', '/static/admin/css/forms.css',
                       ), }
        js = ('/admin/jsi18n',)
        # todo - foreign key to task groups
    class Meta:
        model = Course
        fields = ('name', 'questions_per_student', 'assigned_groups', 'tasks_pool', ) + tuple(BRACKET_LIST) #  'bracket_1'
        labels = {
            # 'assigned_groups': '',
            # 'tasks_pool': ''
            var_name: '' for var_name in CRUTCH
        }
        # widgets = {
        #     'tasks_pool': FilteredSelectMultiple("Tasks", is_stacked=False),
        #     'assigned_groups': FilteredSelectMultiple("Groups", is_stacked=False),
        #     'bracket_1': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_2': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_3': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_4': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_5': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_5': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_5': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_5': FilteredSelectMultiple("", is_stacked=False),
        #     'bracket_5': FilteredSelectMultiple("", is_stacked=False),
        # }#.update({'bracket_1': FilteredSelectMultiple('', is_stacked=True)})
        widgets = {
            var_name: FilteredSelectMultiple(var_name, is_stacked=False, choices=Task.get_all_tasks()) for var_name in CRUTCH
        }

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id')
        super(CourseManagment, self).__init__(*args, **kwargs)

        # self.Meta.widgets = {**self.Meta.widgets, **{br: FilteredSelectMultiple('', is_stacked=True) for br in BRACKET_LIST}}

        brackets = Course.objects.get(id=self.course_id).questions_per_student
        bracket_dict = Course.bracket_dict()

        for i in range(int(brackets) + 1, 31):
            self.fields.pop(bracket_dict[i])
        #print(self.Meta.widgets)
        self.fields['bracket_1'].queryset=Task.objects.all()
        # self.fields['bra_0'] = forms.ModelMultipleChoiceField(queryset=Task.objects.all(),
        #                                     widget=FilteredSelectMultiple("bra 0", is_stacked=False))


        #self.fields.pop('bracket_1')


class CourseManagmentForm(forms.Form):
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

    # class Meta:
    #     model = Course
    #     fields = ('name', 'tasks_pool',)


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


