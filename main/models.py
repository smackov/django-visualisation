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
    name = models.CharField(max_length=20)
    rate = models.FloatField(help_text="Enter the rate value")

    def __str__(self):
        return self.name


class Track(models.Model):
    date = models.DateField()
    id_task = models.ForeignKey("Task", on_delete=models.CASCADE,
                                verbose_name='Task')
    duration = models.IntegerField()
    id_rate = models.ForeignKey("Rate", on_delete=models.CASCADE,
                                verbose_name='Rate')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ('date', 'author', 'id_task')

    def __str__(self):
        return (f'{self.id} - ' + self.id_task.name +
                f' - {self.duration} pom-ro' + f' - {self.date}')


class QuoteManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        if count == 0:
            return None
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Quote(models.Model):
    author = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    objects = QuoteManager()
