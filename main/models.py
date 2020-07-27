from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Rate(models.Model):
    name = models.CharField(max_length=20)
    rate = models.FloatField()

    def __str__(self):
        return self.name

    
class Track(models.Model):
    date = models.DateField()
    id_task = models.ForeignKey("Task", on_delete=models.CASCADE)
    duration = models.IntegerField()
    id_rate = models.ForeignKey("Rate", on_delete=models.CASCADE)




