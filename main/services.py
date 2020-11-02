from django.db.models import Sum, Avg
from .models import Track, Task
from datetime import date, timedelta


# COMMON FUNCTIONS. RECIEVING INFORMATION FROM DB.


def get_week_information(user, added_date=None):
    if not user.is_authenticated:
        return None
    week_date = first_and_last_days_of_week(added_date)
    tracks = Track.objects.filter(
        date__gte=week_date['first_day']
    ).exclude(
        date__gte=week_date['last_day']
    ).filter(
        author=user
    )
    worked_time_in_hours, status_complete, status_complete_css = get_work_info(
        tracks)
    context = {
        'tracks': tracks,
        'worked_time': worked_time_in_hours,
        'status_complete': toFixed(status_complete, digits=0),
        'status_complete_css': toFixed(status_complete_css, digits=0),
        'date': week_date,
        'days': tracks_of_days(tracks, week_date)
    }
    return context


def get_last_four_weeks(user):
    """Return information about last 4 weeks in the form of attributes:

    week_procent_execution, emoji, period_of_week
    """

    day_of_week = date.today() - timedelta(days=7)
    context = []

    for number_week in range(1, 5):

        week_date = first_and_last_days_of_week(added_date=day_of_week)

        tracks = Track.objects.filter(
            date__gte=week_date['first_day']
        ).exclude(
            date__gte=week_date['last_day']
        ).filter(
            author=user
        )

        worked_time_in_hours, status_complete, status_complete_css = get_work_info(
            tracks)
        emoji = get_emoji(status_complete)

        context.append({
            'worked_time': worked_time_in_hours,
            'status_complete': toFixed(status_complete, digits=0),
            'status_complete_css': toFixed(status_complete_css, digits=0),
            'first_day': week_date['first_day'],
            'last_day': week_date['last_day'].strftime('%d %b'),
            'emoji': emoji,
        })

        day_of_week -= timedelta(days=7)
        print(day_of_week)

    return context


def get_work_time_statistic(user):
    """Return worked time statistis.

    Worked time for: 
    - current month, 
    - last month, 
    - ever time.
    """

    _month = date.today().month

    statistic = {
        'current_month': get_worked_time(user, ),
        'last_month': get_worked_time(user, _month-1),
        'ever': get_worked_time(user),
    }
    return statistic


def get_worked_time(user, month):
    pass


def tracks_of_days(tracks, week_date):
    """Return a list about a week.

    The list contains 7 elements (days).
    Each element has 3 subelements: 

    - date (in datetime.date format)
    - tracks(number, track, task, duration) 
    - worked time (total worked time for the day)
    """

    tracks_of_days = []
    day = week_date['first_day']

    while day != week_date['last_day']:
        tracks_of_day = []
        number = 1
        day_tracks = tracks.filter(
            date__gte=day
        ).exclude(
            date__gte=day + timedelta(days=1)
        ).values('id_task').annotate(sum_duration=Sum('duration')).order_by('-sum_duration')

        for track in day_tracks:
            tracks_of_day.append({
                'number': number,
                'track': track,
                'task': Task.objects.get(id=track['id_task']),
                'duration': pomodoros_to_hours(track['sum_duration'])
            })
            number += 1

        tracks_of_days.append({
            'date': day,
            'tracks': tracks_of_day,
            'worked_time': pomodoros_to_hours(day_tracks.aggregate(sum=Sum('duration'))['sum'])
        })
        day += timedelta(days=1)

    return tracks_of_days


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


def first_and_last_days_of_week(added_date):
    """Find first and last days of a week.

    The week is defined by the added date.
    """

    if not added_date:
        added_date = date.today()

    first_day = added_date - timedelta(days=added_date.weekday())
    last_day = first_day + timedelta(days=7)
    return {'first_day': first_day, 'last_day': last_day}

# 2


def days_of_week(added_date):
    if not added_date:
        added_date = date.today()
    days = []
    day = added_date - timedelta(days=added_date.weekday())
    for i in range(7):
        days.append(day)
        day += timedelta(days=1)
    return days

# HELPFUL SECONDARY FUNCTIONS


def pomodoros_to_hours(pomodoros):
    """Transform pomodoro time to usual time (hours, minutes)"""
    if pomodoros:
        hours = pomodoros // 2
        minutes = pomodoros % 2 * 30
    else:
        hours, minutes = 0, 0
    return {'hours': hours, 'minutes': minutes}


def toFixed(numObj, digits=0):
    """Fixes number of float digits after point"""
    return f"{numObj:.{digits}f}"


def get_emoji(procent):
    procent = int(procent)
    if procent <= 0:
        emoji = '😵'
    elif procent < 20:
        emoji = '😥'
    elif procent < 50:
        emoji = '😫'
    elif procent < 80:
        emoji = '😐'
    elif procent < 100:
        emoji = '🤔'
    elif procent < 110:
        emoji = '🔥'
    elif procent < 130:
        emoji = '🏆'
    elif procent >= 130:
        emoji = '🎖'
    return emoji
