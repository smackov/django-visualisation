from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.views.generic import CreateView

from .form import TaskForm, TrackForm
from .models import Task, Track, Rate, Quote
from .services import get_week_information, get_last_four_weeks
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


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'main/task_create.html'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()

            # Add this session variable to say to render UNDO button
            # after redirect to the same page
            self.request.session['enable_undo_button'] = 'True'

        return self.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date_today()
        context['number_day'] = number_day()
        context['quote'] = Quote.objects.random()
        context['tasks'] = Task.objects.filter(author=self.request.user)
        
        # If we came to this view from 'undo task' proccess,
        # we should get session var 'enable_undo_button' = 'True'.
        # If it is we add it to the context to render UNDO button
        if self.request.session.get('enable_undo_button', False) == 'True':
            context['enable_undo_button'] = 'True'
            del self.request.session['enable_undo_button']
        else:
            context['enable_undo_button'] = False
            
        return context


@login_required
def add_track(request):

    if request.method == 'POST':
        form = TrackForm(request.POST, user=request.user)
        if form.is_valid():
            track = form.save(commit=False)
            track.author = request.user
            track.save()

            # Add this session variable to say to render UNDO button
            # after redirect to the same page
            request.session['enable_undo_button'] = 'True'

    form = TrackForm(user=request.user)
    tracks = Track.objects.filter(author=request.user).order_by('-id')[:10]

    # If we came to this view from 'undo track' proccess,
    # we should get session var 'enable_undo_button' = 'True'.
    # If it is we add it to the context to render UNDO button
    if request.session.get('enable_undo_button', False) == 'True':
        enable_undo_button = 'True'
        del request.session['enable_undo_button']
    else:
        enable_undo_button = False

    context = {
        'form': form,
        'tracks': tracks,
        'date': date_today(),
        'number_day': number_day(),
        'quote': Quote.objects.random(),
        'enable_undo_button': enable_undo_button,
    }
    return render(request, 'main/add_track.html', context)


@login_required
def track_undo_insert(request):
    """This view delete the last inserted track from db.

    (i.e. UNDO function)."""
    if request.method == 'POST':
        # Get all user tracks
        user_tracks = Track.objects.filter(author=request.user)
        # Get the last inserted track and delete it
        last_index = user_tracks.aggregate(Max('id'))['id__max']
        user_tracks.filter(id=last_index).delete()

    return redirect('add_track')


@login_required
def task_undo_insert(request):
    """This view delete the last inserted task from db.

    (i.e. UNDO function)."""
    if request.method == 'POST':
        # Get all user tracks
        user_tasks = Task.objects.filter(author=request.user)
        # Get the last inserted track and delete it
        last_index = user_tasks.aggregate(Max('id'))['id__max']
        user_tasks.filter(id=last_index).delete()

    return redirect('add_task')


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
