from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bookings.models import Booking
from users.models import SavedDestination, User
from destinations.models import Destination


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def saved(request):
    saved_destinations = SavedDestination.objects.filter(user=request.user)
    destinations = [saved.destination for saved in saved_destinations]

    # Check if the destination is saved by the requesting user
    for destination in destinations:
        destination.is_saved_by_user = destination.saveddestination_set.filter(user=request.user).exists()

    if request.method == 'POST' and 'delete' in request.POST:
        current_user = request.user
        destination = Destination.objects.get(id=request.POST['destination_id'])
        saved_destination = SavedDestination.objects.get(user=current_user, destination=destination)
        saved_destination.delete()
        return redirect('saved')

    return render(request, 'users/saved.html', {'destinations': destinations})


def profile(request, username):
    context = {}
    user = User.objects.get(username=username)
    context['user'] = user

    if user.is_host:
        user_listings = Destination.objects.filter(host=user).order_by('name')
        context['user_listings'] = user_listings

    return render(request, 'users/profile.html', context)


@login_required
def host(request):
    destinations = Destination.objects.filter(host=request.user)

    # Fetch all bookings for the user's destinations
    bookings = Booking.objects.filter(destination__in=destinations)

    # Filter bookings based on boolean properties
    currently_hosting = [booking for booking in bookings if booking.in_progress()]
    past_bookings = [booking for booking in bookings if booking.is_finished()]
    upcoming_bookings = [booking for booking in bookings if booking.is_upcoming()]
    pending_bookings = bookings.filter(status='Pending')

    context = {
        'currently_hosting': currently_hosting,
        'past_bookings': past_bookings,
        'upcoming_bookings': upcoming_bookings,
        'pending_bookings': pending_bookings
    }
    return render(request, 'users/hosting.html', context)


def listings(request):
    listing_destinations = Destination.objects.filter(host=request.user).order_by('name')

    return render(request, 'users/listings.html', {'listing_destinations': listing_destinations})
