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
            task = form.save(commit=False)
            task.author = request.user
            task.save()
    form = TaskForm()
    tasks = Task.objects.filter(author=request.user)
    context = {
        'form': form,
        'tasks': tasks,
        'date': date_today(),
    }
    return render(request, 'main/add_task.html', context)

@login_required
def add_track(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, user=request.user)
        if form.is_valid():
            track = form.save(commit=False)
            track.author = request.user
            track.save()
    form = TrackForm(user=request.user)
    tracks = Track.objects.filter(author=request.user).order_by('-date')
    tasks = Task.objects.filter(author=request.user)
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
