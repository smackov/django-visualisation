from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def add_track(request):
    return render(request, 'main/add_track.html')

