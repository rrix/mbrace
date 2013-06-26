from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.forms import *
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login

import json


def index(request):
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Hugger.objects.create(user=new_user)
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreateForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


@login_required
def profile(request):
    form = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.hugger)
        if form.is_valid():
            hugger = form.save()
    else:
        form = ProfileForm(instance=request.user.hugger)

    return render(request, "core/profile.html", {'form': form})


@login_required
def new_hug(request):
    hugger = request.user.hugger
    new_hug = Meeting.objects.create(user_in_need=hugger)


@login_required
def update_location(request):
    hugger = request.user.hugger
    json_encoded = json.dumps(request.GET)
    hugger.last_location = json_encoded
    hugger.save
