"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_task', views.TaskCreateView.as_view(), name='add_task'),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name='update_task'),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name='delete_task'),
    path('add_track', views.add_track, name='add_track'),
    path('track/<int:pk>/update', views.TrackUpdateView.as_view(), name='update_track'),
    path('track_undo_insert', views.track_undo_insert, name='track_undo_insert'),
    path('task_undo_insert', views.task_undo_insert, name='task_undo_insert'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
