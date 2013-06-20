from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.forms import UserCreateForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login


def index(request):
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreateForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required
def profile(request):
    return render(request, "core/dashboard.html")
