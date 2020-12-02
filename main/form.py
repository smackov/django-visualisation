from datetime import date

from django.forms import (ChoiceField, ModelForm, DateInput, Select,
                          NumberInput, BaseModelFormSet, TextInput)
from django import forms
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

    # GEEKS_CHOICES = (
    #     ("1", "One"),
    #     ("2", "Two"),
    #     ("3", "Three"),
    #     ("4", "Four"),
    #     ("5", "Five"),
    # )

    # id_task = forms.ChoiceField(choices = GEEKS_CHOICES)

    id_task = forms.ModelChoiceField(
        widget=Select(attrs={'class': 'form-control', 'autofocus': 1, }),
        empty_label='Select the task', queryset=None, to_field_name="")
    id_rate = forms.ModelChoiceField(
        widget=Select(attrs={'class': 'form-control'}),
        queryset=Rate.objects.all(), empty_label=None, to_field_name="")

    def __init__(self, *args, **kwargs):
        # Get current user
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Set appropriate queryset for current user
        self.fields['id_task'].queryset = Task.objects.filter(author=user)

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
