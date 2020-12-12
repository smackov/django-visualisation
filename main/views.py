from datetime import date

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Max
from django.views.generic import CreateView, UpdateView, DeleteView

from .form import TaskForm, TrackForm
from .models import Task, Track, Rate, Quote
from .services import get_week_information, get_last_four_weeks
from .user_tracks import UserTracks


def index(request):
    "The general page with common statistic."
    context = {}

    if request.user.is_authenticated:
        userTracks = UserTracks(request.user)
        context = {
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
    """
    This class based view contains task form and list of last 10
    created tasks.
    """
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


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'main/task_update.html'
    form_class = TaskForm
    success_url = reverse_lazy('add_task')
    

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'main/task_delete.html'
    success_url = reverse_lazy('add_task')


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
        'enable_undo_button': enable_undo_button,
    }
    return render(request, 'main/add_track.html', context)


class TrackUpdateView(LoginRequiredMixin, UpdateView):
    model = Track
    template_name = 'main/track_update.html'
    form_class = TrackForm
    success_url = reverse_lazy('add_track')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


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
