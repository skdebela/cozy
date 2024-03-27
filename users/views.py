from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import SavedDestination, User
from destinations.models import Destination


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def saved(request):
    saved_destinations = SavedDestination.objects.filter(user=request.user)

    return render(request, 'users/saved.html', {'saved_destinations': saved_destinations})


def profile(request, username):
    context = {}
    user = User.objects.get(username=username)
    context['user'] = user

    if user.is_host:
        user_listings = Destination.objects.filter(host=user).order_by('name')
        context['user_listings'] = user_listings

    return render(request, 'users/profile.html', context)


def listings(request):
    listing_destinations = Destination.objects.filter(host=request.user).order_by('name')

    return render(request, 'users/listings.html', {'listing_destinations': listing_destinations})
