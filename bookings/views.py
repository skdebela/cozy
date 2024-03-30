from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from bookings.forms import BookingForm
from bookings.models import Booking
from destinations.models import Destination
from users.models import User


@login_required
def book(request, destination_id, destination_name, booking_id):
    destination = Destination.objects.get(id=destination_id)
    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        booking.guest = request.user
        if booking.destination.instant_book:
            booking.status = 'Approved'
        booking.save()
        return redirect('booking_successful', booking_id=booking_id)

    return render(request, 'booking/booking.html', {'booking': booking, 'destination': destination})


@login_required
def booking_successful(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking/booking_successful.html', {'booking': booking})


@login_required
def approve_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        if booking.destination.host == request.user:
            booking.status = 'Approved'
            booking.save()
            return redirect('hosting')
