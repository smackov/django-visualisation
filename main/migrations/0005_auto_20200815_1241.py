# Generated by Django 3.0.5 on 2020-08-15 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200730_0936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['author', 'name']},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ('date', 'author', 'id_task')},
        ),
        migrations.AlterField(
            model_name='track',
            name='duration',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='track',
            name='id_rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Rate', verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='track',
            name='id_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Task', verbose_name='Task'),
        ),
    ]
