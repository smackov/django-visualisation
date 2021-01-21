from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import GuestModeCounter
from .services import populate_user


def signup(request):
    "The sign up view"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def guest_mode(request):
    """The guest mode - sign in as guest user without registration.

    When user choose this mode the new guest user is created. Then for
    this new guest user the view populates db by tracks and authorizate
    user."""
    try:
        # Get counter from db
        guest_counter = GuestModeCounter.objects.get(id=1)
    except GuestModeCounter.DoesNotExist:
        # Create counter if it doesn't exist and get it
        GuestModeCounter.objects.create()
        guest_counter = GuestModeCounter.objects.get(id=1)
    # Get counter value from db
    counter = guest_counter.counter
    # Create new guest user with 'counter' suffix
    user = User.objects.create_user(username=f'Guest {counter}',
                                    password=f'KJn424kNKJl{counter}')
    # Populate new guest account by tasks and tracks
    populate_user(user)
    # Login new user
    login(request, user)
    # Grow our counter for nest guest users
    guest_counter.counter += 1
    guest_counter.save()
    return redirect('index')
