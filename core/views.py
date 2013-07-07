from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from core.forms import *
from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login
from gmapi import maps
from django.contrib import messages

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
    def get_hugs(friend):
        return friend.requestor_set.all().order_by('-id')[0]

    nearby = Meeting.nearby(request.user)
    friends = Hugger.objects.filter(friend_objects__id=request.user.id).order_by('last_hug_date')
    friend_hugs = map(get_hugs, friends)

    return render(request, "core/dashboard.html",
                  {'nearby': nearby,
                   'current_user': request.user,
                   'friend_hugs': friend_hugs})


@login_required
def profile(request, uid):
    # XXX I suppose I need to audit this?
    uid = int(uid)
    if uid == request.user.id:
        form = None

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                hugger = form.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Your profile has been updated.')
        else:
            form = ProfileForm(instance=request.user)

        return render(request, "core/profile.html",
                      {'form': form, 'username': uid})
    else:
        return render(request, "core/show_profile.html",
                      {'user': Hugger.objects.get(id=uid)})


@login_required
def new_hug(request):
    import datetime
    hugger = request.user

    if hugger.last_location != "":
        new_hug = Meeting.objects.create(user_in_need=hugger)
        hugger.last_hug_date = datetime.datetime.now()
        hugger.save()
        return HttpResponseRedirect(reverse('edit_hug', args=(new_hug.id,)))
    else:
        messages.add_message(request, messages.ERROR,
                             'Your browser does not seem to have geolocation enabled so we cannot reliably pinpoint your location!')
        return HttpResponseRedirect(reverse('dashboard'))


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

    # Let's make sure someone we know owns this object!
    if (hug.user_delivering is None) or (hug.user_delivering is not None and request.user == hug.user_delivering) or (request.user == hug.user_in_need):
        if 'action' in request.GET:
            action = request.GET['action']
            # do something interesting here
            if action == 'join':
                if request.user.has_open_hugs():
                    messages.add_message(request, messages.ERROR,
                                         'You are already meeting up with someone for hugs!')
                else:
                    hug.user_delivering = request.user
                    hug.save()
                    messages.add_message(request, messages.INFO,
                                         'Cool, we will let %s know!' % hug.user_in_need.nickname)
            if action == 'delete':
                if request.user == hug.user_in_need:
                    hug.delete()
                    messages.add_message(request, messages.INFO,
                                          'Alright, let us know if you need a hug, okay?')
                return HttpResponseRedirect(reverse('dashboard'))
            if action == 'clear_deliverer':
                hug.user_delivering == None
                hug.save()
                messages.add_message(request, messages.INFO,
                                     'Cool, we will let %s know!' % hug.user_in_need.nickname)
                return HttpResponseRedirect(reverse('dashboard'))

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
                       'form': MapForm(initial={'map': gmap}),
                       'current_user': request.user})
    else:
        messages.add_message(request, messages.ERROR,
                              "This page doesn't belong to you!" )
        return HttpResponseRedirect(reverse('dashboard'))

@login_required
def new_message(request, hug_id):
    hug = Meeting.objects.get(id=int(hug_id))
    if (request.user == hug.user_in_need) or (request.user == hug.user_delivering):
        message = Message.objects.create(text=request.POST['text'],
                                         meeting=hug,
                                         sender=request.user)
        message.save()
        return HttpResponseRedirect(reverse('edit_hug', args=(int(hug_id),)))
    else:
        messages.add_message(request, messages.ERROR,
                             'You cannot send messages to that meeting!')
        return HttpResponseRedirect(reverse('dashboard'))
