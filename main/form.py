from datetime import date

from django.forms import (ModelForm, DateInput, Select, 
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['id_task'].queryset = Task.objects.filter(author=user)
        print(Task.objects.filter(author=user))
        # self.initial['id_task'] = 'default value'

    class Meta:
        model = Track
        fields = ('id_task', 'duration', 'id_rate', 'date')
        widgets = {
            'id_task': Select(
                attrs={'class': 'form-control',
                       'autofocus': 1, 
                       'placeholder': 'Pomodoros'}),
            'duration': NumberInput(
                attrs={'class': 'form-control',
                       'min': 1, 'max': 20,
                       'value': False,
                       'class': 'form-control',
                       'placeholder': 'Pomodoros'}),
            'id_rate': Select(
                attrs={'class': 'form-control'}), 
            'date': DateInput(
                attrs={'class': 'form-control',
                       'type': 'date',
                       'value': date.today().isoformat()}),
        }


class RateForm(ModelForm):
    
    class Meta:
        model = Rate
        fields = ['name', 'rate', ]
