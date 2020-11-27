from datetime import date

from django.forms import (ChoiceField, ModelForm, DateInput, Select,
                          NumberInput, BaseModelFormSet, TextInput)
from django.utils.translation import gettext_lazy as _

from .models import Task, Track, Rate


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', ]
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control',
                       'autofocus': 1,
                       'placeholder': 'A new task ...'})
        }


class TrackForm(ModelForm):

    id_task = ChoiceField(
        widget=Select(attrs={'class': 'form-control', 'autofocus': 1, }))
    id_rate = ChoiceField(widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Get current user
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Create choices for 'id_task' field
        tasks_choices = list(map(lambda task: (f'{task.id}', f'{task.name}'),
                                 list(Task.objects.filter(author=user))))
        # Add default choice for Select widget
        tasks_choices.insert(0, ('default', 'Select the task'))
        self.fields['id_task'].initial = 'default'
        self.fields['id_task'].choices = tasks_choices

        # Create choices for 'id_rate' field
        self.fields['id_rate'].choices = list(map(lambda rate: (f'{rate.id}', f'{rate.name}'),
                                 list(Rate.objects.all())))
        # Add default choice for Select widget
        self.fields['id_rate'].initial = f'{Rate.objects.get(name="Good").id}'
        
    class Meta:
        model = Track
        fields = ('duration', 'date')
        widgets = {
            'duration': NumberInput(
                attrs={'class': 'form-control',
                       'min': 1, 'max': 20,
                       'value': False,
                       'class': 'form-control',
                       'placeholder': 'Pomodoros'}),
            'date': DateInput(
                attrs={'class': 'form-control',
                       'type': 'date',
                       'value': date.today().isoformat()}),
        }


class RateForm(ModelForm):

    class Meta:
        model = Rate
        fields = ['name', 'rate', ]
