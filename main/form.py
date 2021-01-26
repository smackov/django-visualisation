from datetime import date

from django.forms import DateInput, Select, NumberInput, TextInput
from django import forms

from .models import Task, Track, Rate


class TaskForm(forms.ModelForm):
    "The form for objects of the Task class"

    class Meta:
        model = Task
        fields = ['name', ]
        widgets = {'name': TextInput(attrs={'class': 'form-control', 'autofocus': 1,
                                            'placeholder': 'A new task ...'})}


class TrackForm(forms.ModelForm):
    "The form for objects of the Track class"

    id_task = forms.ModelChoiceField(
        widget=Select(attrs={'class': 'form-control', 'autofocus': 1, }),
        queryset=None, empty_label='Select the task', to_field_name="")
    id_rate = forms.ModelChoiceField(
        widget=Select(attrs={'class': 'form-control'}),
        queryset=Rate.objects.all(), empty_label=None, to_field_name="")

    class Meta:
        model = Track
        fields = ('duration', 'date', 'id_task', 'id_rate')
        widgets = {
            'duration': NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 20,
                       'value': False, 'class': 'form-control',
                       'placeholder': 'Pomodoros'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'})}

    def __init__(self, *args, **kwargs):
        # Get current user
        user = kwargs.pop('user')
        # Call super __init__ function
        super().__init__(*args, **kwargs)
        # Set date
        self.date = date.today().isoformat()
        # Set appropriate queryset containing only Tasks belong to the
        # current User
        self.fields['id_task'].queryset = Task.objects.filter(author=user)
        self.fields['id_rate'].initial = Rate.objects.get(name='Good')
        print(dir(self.fields['date']))
        self.fields['date'].initial = date.today().isoformat()
