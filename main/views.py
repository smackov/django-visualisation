from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .form import TaskForm, TrackForm, RateForm
from .models import Task, Track, Rate, Quote
from .services import (
    get_week_information,
    get_last_four_weeks,
)
from .user_tracks import UserTracks


def index(request):
    "The general page with common statistic."

    context = {
        'date': date_today(),
        'number_day': number_day(),
        'quote': Quote.objects.random(),
    }
    

    if request.user.is_authenticated:
        userTracks = UserTracks(request.user)
        context = {
            'date': date_today(),
            'number_day': number_day(),
            'quote': Quote.objects.random(),
            'week_data': get_week_information(request.user),
            'last_weeks': get_last_four_weeks(request.user),
            'statistic': {
                'current_week': userTracks.work_time_current_week(),
                'current_month': userTracks.work_time_current_month(),
                'last_month': userTracks.work_time_last_month(),
                'for_ever': userTracks.work_time_for_ever(),
            },
            'current_week': userTracks.current_week_detail(),
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
        'number_day': number_day(),
        'quote': Quote.objects.random(),
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
    tracks = Track.objects.filter(author=request.user).order_by('-id')[:10]
    
    context = {
        'form': form,
        'tracks': tracks,
        'date': date_today(),
        'number_day': number_day(),
        'quote': Quote.objects.random(),
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
        'number_day': number_day(),
        'quote': Quote.objects.random(),
    }
    return render(request, 'main/add_rate.html', context)


# SUPPORT FUNCTIONS


def date_today():
    """It return a date in accurate for pages format
    
    date_today() --> 'Saturday 14 November'
    """
    return date.today().strftime('%A %d %B')


def number_day():
    """The number day of year
    
    if today 01.01.2020 (the first day of year)
    number_day() --> 1
    
    if today 05.07.2020 (the arbitrary day of year)
    number_day() --> 187
    
    if today 31.12.2020 (the last day of year)
    number_day() --> 366 (leap year)
    """
    return (date.today().toordinal() -
            date(date.today().year, 1, 1).toordinal() + 1)
