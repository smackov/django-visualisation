from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=40)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['author', 'name']


class Rate(models.Model):
    name = models.CharField(max_length=20)
    rate = models.FloatField(help_text="Enter the rate value")

    def __str__(self):
        return self.name

    
class Track(models.Model):
    date = models.DateField()
    id_task = models.ForeignKey("Task", on_delete=models.CASCADE, verbose_name='Task')
    duration = models.IntegerField(default=1)
    id_rate = models.ForeignKey("Rate", on_delete=models.CASCADE, verbose_name='Rate')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date', 'author', 'id_task')

    def __str__(self):
        return f'{self.id} - ' + self.id_task.name + f' - {self.duration} pom-ro' + f' - {self.date}'



