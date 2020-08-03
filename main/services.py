from django.db.models import Sum
from .models import Track
from datetime import date, timedelta


def get_week_information(user, added_date=None):
    if not user.is_authenticated:
        return None
    period_week = get_period_week(added_date)
    tracks = Track.objects.filter(
        date__gte=period_week['first_day']
    ).exclude(
        date__gte=period_week['last_day']
    ).filter(
        author=user
    )
    worked_time_in_hours, status_complete, status_complete_css = get_work_info(tracks)
    context = {
        'tracks': tracks, 
        'worked_time': worked_time_in_hours, 
        'status_complete': toFixed(status_complete, digits=0),
        'status_complete_css': toFixed(status_complete_css, digits=0),
    }
    return context

def get_work_info(tracks):
    worked_time = tracks.aggregate(Sum('duration'))['duration__sum']
    if worked_time == None:
        worked_time = 0
    worked_time_in_hours = pomodoros_to_hours(worked_time)
    status_complete = worked_time / 60 * 100
    if status_complete > 100: 
        status_complete_css = 100
    else:
        status_complete_css = status_complete
    return worked_time_in_hours, status_complete, status_complete_css


def get_period_week(added_date):
    if not added_date:
        added_date = date.today()
    first_day = added_date - timedelta(days=added_date.weekday())
    last_day = first_day + timedelta(days=7)
    return {'first_day': first_day, 'last_day': last_day}


def pomodoros_to_hours(pomodoros):
    hours = pomodoros // 2
    minutes = pomodoros % 2 * 30
    return {'hours': hours, 'minutes': minutes}


def toFixed(numObj, digits=0):
  # Fixed number of float digits after point 
    return f"{numObj:.{digits}f}"

