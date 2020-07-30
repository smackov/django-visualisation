from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import TaskForm, TrackForm, RateForm
from .models import Task, Track, Rate

from datetime import date

# Create your views here.
def date_today():
    return date.today().strftime('%A %d %B')


def index(request):
    context = {
        'date': date_today(),
    }
    return render(request, 'main/index.html', context)

@login_required
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

@login_required
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


@login_required
def add_rate(request):
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
    form = RateForm()
    rates = Rate.objects.all()
    context = {
        'form': form,
        'rates': rates,
        'date': date_today(),
    }
    return render(request, 'main/add_rate.html', context)
