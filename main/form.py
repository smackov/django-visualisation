from django.forms import ModelForm, DateInput, Select, NumberInput, BaseModelFormSet
from .models import Task, Track, Rate

from datetime import date

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name',]


class TrackForm(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['id_task'].queryset = Task.objects.filter(author=user)

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


class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['name', 'rate',]
