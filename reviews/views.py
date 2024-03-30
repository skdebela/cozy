from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from bookings.models import Booking
from destinations.models import Destination
from reviews.forms import ReviewForm


@login_required
def review(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)
    current_user = request.user
    if request.method == 'POST':
        confirmed_guests = Booking.objects.filter(destination=destination, guest=current_user, is_completed=True)
        if current_user in confirmed_guests:
            review_form = ReviewForm(request.POST)
            review_form.user = current_user
            review_form.destination = destination
            review_form.save()

            return redirect('details', destination_id=destination_id, destination_name=destination_name)
