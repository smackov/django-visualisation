from django.shortcuts import render, redirect
from .form import TaskForm, TrackForm
from .models import Task, Track

from datetime import date

# Create your views here.
def date_today():
    return date.today().strftime('%A %d %B')


def index(request):
    return render(request, 'main/index.html', {'date': date_today()})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST) 
        if form.is_valid():
            form.save()
    form = TaskForm()
    tasks = Task.objects.all()
    context = {
        'form': form,
        'tasks': tasks,
        'date': date_today(),
    }
    return render(request, 'main/add_task.html', context)


def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            form.save()
    form = TrackForm()
    tracks = Track.objects.order_by('-date')
    tasks = Task.objects.all()
    context = {
        'form': form,
        'tracks': tracks,
        'tasks': tasks,
        'date': date_today(),
    }
    return render(request, 'main/add_track.html', context)

