from datetime import date, timedelta
from random import choice

from main.models import Task, Track, Rate


def populate_user(user):
    """Populate guest user account by tasks and tracks.

    Create brief set of tasks for defined guest user.
    Create tracks for last 5 weeks for defined guest user."""
    # Create 3 tasks for guest user
    tasks = ('English', 'Programming', 'Python')
    for task in tasks:
        Task.objects.create(name=task, author=user)
    # Get all rates from db
    rates = Rate.objects.all()
    # Get all tasks that belongs to guest user
    tasks = Task.objects.filter(author=user)
    # Create set of variants for duration field in Task instances
    # some values are repeated because we user randome.choice function
    # to choose one value of defined collection. Then when a value is 
    # repeated the chance of dropping this value increases
    durations = (1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6)
    # Create tracks for last 5 weeks for guest user
    today = date.today()
    for i in range(5*7):
        # '5*7' - number of days in defined period (last 5 weeks)
        # In each iteration we low today variable by 1 day
        today -= timedelta(days=1)
        # For each task create track for today date
        for task in tasks:
            Track.objects.create(date=today, id_task=task, author=user,
                                 id_rate=choice(rates), duration=choice(durations))
