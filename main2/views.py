from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Track, Rate

from datetime import date

# Create your views here.
def date_today():
    return date.today().strftime('%A %d %B')
def number_day():
    return date.today().toordinal() - date(date.today().year, 1, 1).toordinal() + 1

def index(request):
    context = {
        'date': date_today(),
        'number_day': number_day(),
        # 'week_data': get_week_information(request.user),
    }
    return render(request, 'main/index.html', context)

