from random import randint

from django.db import models
from django.conf import settings
from django.db.models.aggregates import Count
from django.urls import reverse


class Task(models.Model):
    """
    Task - what we can do.

    For example, we can learn English so we can create the 'English' 
    task. Also we  can  divide  this  task  to  some  smaller tasks: 
    'Learning words', 'Whatching english videos', 'English grammer',
    and so on.
    """
    name = models.CharField(max_length=40)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['author', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("update_task", kwargs={"pk": self.pk})


class Rate(models.Model):
    """
    Rate - it is how good we can compete the track.

    For example, bad, good or perfect. The value of rate will influence
    to an user score (it will be implemented in the future).
    """
    name = models.CharField(max_length=20)
    rate = models.FloatField(help_text="Enter the rate value")

    def __str__(self):
        return self.name


class Track(models.Model):
    """
    Track - it is finished period of time that was spent to a task.

    For example, we had been learning English for 2 hours (4 pomodoros) today.
    So we can create new completed track with specified charechteristics: 
        date = today, task = English, duration = 4 pomodoros,
        rate = good, author = me
    """
    date = models.DateField()
    id_task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        verbose_name='Task'
    )
    duration = models.IntegerField()
    id_rate = models.ForeignKey(
        "Rate",
        on_delete=models.CASCADE,
        verbose_name='Rate'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('date', 'author', 'id_task')

    def __str__(self):
        return (f'{self.id} - ' + self.id_task.name +
                f' - {self.duration} pom-ro' + f' - {self.date}')

    # def get_absolute_url(self):
    #     return reverse("update_track", kwargs={"pk": self.pk})


class QuoteManager(models.Manager):
    "The queryset manager of Quote class"

    def random(self):
        "Get random quote from database"
        count = self.aggregate(count=Count('id'))['count']
        if count == 0:
            return None
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Quote(models.Model):
    """
    Quotes from this class are shown in all pages of this webapplication.
    """
    author = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    objects = QuoteManager()
