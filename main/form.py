from django.forms import ModelForm, DateInput, Select, NumberInput
from .models import Task, Track

from datetime import date

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name',]


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ['id_task', 'duration', 'id_rate', 'date',]
        today = date.today().isoformat()
        widgets = {
            'id_task': Select(attrs={'size': Task.objects.count()+1, 'autofocus': 1}),
            'id_rate': Select(attrs={'size': 4}),
            'date': DateInput(attrs={'type': 'date', 'value': today}),
            'duration': NumberInput(attrs={'value': 1})
        }

