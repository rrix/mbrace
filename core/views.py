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

import datetime
import json


def index(request):
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.hugger = Hugger.objects.create()
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
        all_hugs = friend.requestor_set.all().order_by('-id')
        if len(all_hugs) > 0:
            return all_hugs[0]
        return None

    nearby = Meeting.nearby(request.user)
    hugger = Hugger.objects.get(user=request.user)
    friends = hugger.friend_objects.order_by('last_hug_date')
    friend_hugs = filter(None, map(get_hugs, friends))

    return render(request, "core/dashboard.html",
                  {'nearby': nearby,
                   'current_user': hugger,
                   'friend_hugs': friend_hugs})


@login_required
def profile(request, uid):
    # XXX I suppose I need to audit this?
    uid = int(uid)
    if uid == request.user.id:
        form = None

        if request.method == 'POST':
            hugger = Hugger.objects.get(user=request.user)
            form = ProfileForm(request.POST, instance=hugger)
            if form.is_valid():
                hugger = form.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Your profile has been updated.')
        else:
            hugger = Hugger.objects.get(user=request.user)
            form = ProfileForm(instance=hugger)

        return render(request, "core/profile.html",
                      {'form': form,
                       'username': uid,
                       'user': request.user})
    else:
        return render(request, "core/show_profile.html",
                      {'user': Hugger.objects.get(id=uid)})


@login_required
def new_hug(request):
    hugger = Hugger.objects.get(user=request.user)

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
    hugger = Hugger.objects.get(user=request.user)
    json_encoded = json.dumps(request.GET)
    hugger.last_location = json_encoded
    hugger.save()

    return HttpResponse("")


@login_required
def edit_hug(request, hug_id):
    hug_id = int(hug_id)
    hug = Meeting.objects.get(id=hug_id)
    user_hug = Hugger.objects.get(user=request.user)

    # Let's make sure someone we know owns this object!
    if (hug.user_delivering is None) or (hug.user_delivering is not None and user_hug == hug.user_delivering) or (user_hug == hug.user_in_need):
        if 'action' in request.GET:
            action = request.GET['action']
            # do something interesting here
            if action == 'join':
                if user_hug.has_open_hugs():
                    messages.add_message(request, messages.ERROR,
                                         'You are already meeting up with someone for hugs!')
                else:
                    hug.user_delivering = user_hug
                    hug.save()
                    messages.add_message(request, messages.INFO,
                                         'Cool, we will let %s know!' % hug.user_in_need.username)
                return HttpResponseRedirect(reverse('edit_hug', args=(hug_id,)))
            if action == 'delete':
                if user_hug == hug.user_in_need:
                    hug.delete()
                    messages.add_message(request, messages.INFO,
                                         'Alright, let us know if you need a hug, okay?')
                return HttpResponseRedirect(reverse('dashboard'))
            if action == 'clear_deliverer':
                hug.user_delivering == None
                hug.save()
                messages.add_message(request, messages.INFO,
                                     'Cool, we will let %s know!' % hug.user_in_need.username)
                return HttpResponseRedirect(reverse('dashboard'))

        u1_location_data = json.loads(hug.user_in_need.last_location)
        u1_lat = float(u1_location_data['latitude'])
        u1_lon = float(u1_location_data['longitude'])

        if hug.user_delivering is not None:
            u2_location_data = json.loads(hug.user_delivering.last_location)
            u2_lat = float(u2_location_data['latitude'])
            u2_lon = float(u2_location_data['longitude'])
            # set icon here
        else:
            u2_location_data = json.loads(user_hug.last_location)
            u2_lat = float(u2_location_data['latitude'])
            u2_lon = float(u2_location_data['longitude'])
            # set icon here

        center_lat = u1_lat - (u1_lat-u2_lat)/2
        center_lon = u1_lon - (u1_lon-u2_lon)/2

        gmap = maps.Map(opts={
            'center': maps.LatLng(center_lat, center_lon),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 15,
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

        user2_marker = maps.Marker(opts={
            'map': gmap,
            'position': maps.LatLng(u2_lat, u2_lon)
            #, 'icon': static asset to image
        })

        return render(request, "core/edit_hug.html",
                      {'hug':  hug,
                       'form': MapForm(initial={'map': gmap}),
                       'current_user': user_hug})
    else:
        messages.add_message(request, messages.ERROR,
                             "This page doesn't belong to you!")
        return HttpResponseRedirect(reverse('dashboard'))


@login_required
def new_message(request, hug_id):
    hug = Meeting.objects.get(id=int(hug_id))
    user_hug = Hugger.objects.get(user=request.user)

    if (user_hug == hug.user_in_need) or (user_hug == hug.user_delivering):
        message = Message.objects.create(text=request.POST['text'],
                                         meeting=hug,
                                         sender=user_hug)
        message.save()
        return HttpResponseRedirect(reverse('edit_hug', args=(int(hug_id),)))
    else:
        messages.add_message(request, messages.ERROR,
                             'You cannot send messages to that meeting!')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required
def send_invite(request):
    hugger = Hugger.objects.get(user=request.user)

    if hugger.invite_count < 0:
        messages.add_message(request, messages.ERROR,
                             'You do not have any available invitations yet!  Hold tight, we are rolling them out as we can.')
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        if request.method == 'GET':
            invite_form = InviteForm()
            invitations = hugger.sent_invite_set.all()

            return render(request, 'core/invite_form.html',
                          {'form': invite_form,
                           'user': request.user,
                           'hugger': hugger,
                           'invitations': invitations})
        elif request.method == 'POST':
            form = InviteForm(request.POST)
            if form.is_valid():
                invitation = form.save(hugger=hugger)
                invitation.send()
                messages.add_message(request, messages.SUCCESS,
                                     'Your invitation will arrive shortly. Hug on!')
            else:
                messages.add_message(request, messages.ERROR,
                                     "For some reason we couldn't send that invite! :(")

            return HttpResponseRedirect(reverse('dashboard'))
