from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from core.forms import *
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from gmapi import maps

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
        return render(request, "core/show_profile.html",
                      {'user': Hugger.objects.get(uid)})


@login_required
def new_hug(request):
    hugger = request.user
    new_hug = Meeting.objects.create(user_in_need=hugger)

    return HttpResponseRedirect(reverse('edit_hug', args=(new_hug.id,)))


@login_required
def update_location(request):
    hugger = request.user
    json_encoded = json.dumps(request.GET)
    hugger.last_location = json_encoded
    hugger.save()

    return HttpResponse("")


@login_required
def edit_hug(request, hug_id):
    hug_id = int(hug_id)
    hug = Meeting.objects.get(id=hug_id)

    u1_location_data = json.loads(hug.user_in_need.last_location)
    u1_lat = float(u1_location_data['coords[latitude]'])
    u1_lon = float(u1_location_data['coords[longitude]'])

    gmap = maps.Map(opts={
        'center': maps.LatLng(u1_lat, u1_lon),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 16,
        'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })

    # Marker for the User in Need
    user1_marker = maps.Marker(opts={
        'map': gmap,
        'position': maps.LatLng(u1_lat, u1_lon)
        #, 'icon': static asset to image
    })

    if hug.user_delivering is not None:
        u2_location_data = json.loads(hug.user_delivering.last_location)
        u2_lat = float(u2_location_data['coords[latitude]'])
        u2_lon = float(u2_location_data['coords[longitude]'])
        # set icon here
    else:
        u2_location_data = json.loads(request.user.last_location)
        u2_lat = float(u2_location_data['coords[latitude]'])
        u2_lon = float(u2_location_data['coords[longitude]'])
        # set icon here

    user2_marker = maps.Marker(opts={
        'map': gmap,
        'position': maps.LatLng(u2_lat, u2_lon)
        #, 'icon': static asset to image
    })

    return render(request, "core/edit_hug.html",
                  {'hug':  hug,
                   'form': MapForm(initial={'map': gmap})})
