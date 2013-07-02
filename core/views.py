from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.forms import *
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
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
    nearby = Meeting.nearby(request.user)
    return render(request, "core/dashboard.html",
                  {'nearby': nearby, 'current_user': request.user})


@login_required
def profile(request, uid):
    # XXX I suppose I need to audit this?
    uid = int(uid)
    if uid == request.user.id:
        form_to_use = None
        form = None
        if request.user.name is not None:
            form_to_use = PartialProfileForm
        else:
            form_to_use = ProfileForm

        if request.method == 'POST':
            form = form_to_use(request.POST, instance=request.user)
            if form.is_valid():
                hugger = form.save()
        else:
            form = form_to_use(instance=request.user)

        return render(request, "core/profile.html",
                      {'form': form, 'username': uid})
    else:
        render(request, "core/show_profile.html",
               {'user': Hugger.objects.get(uid)})


@login_required
def new_hug(request):
    hugger = request.user
    new_hug = Meeting.objects.create(user_in_need=hugger)

    return HttpResponse("")


@login_required
def update_location(request):
    hugger = request.user.hugger
    json_encoded = json.dumps(request.GET)
    hugger.last_location = json_encoded
    hugger.save

    return HttpResponse("")
