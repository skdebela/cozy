from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from bookings.forms import BookingForm
from destinations.models import Destination
from destinations.forms import DestinationSearchForm, DestinationForm, PhotoFormSet
from users.models import User, SavedDestination


def home_view(request):
    destinations = Destination.objects.all()
    search_form = DestinationSearchForm()

    if request.user.is_authenticated:
        for destination in destinations:
            destination.is_saved_by_user = destination.saveddestination_set.filter(user=request.user).exists()

    context = {
        'destinations': destinations,
        'search_form': search_form
    }

    if request.user.is_authenticated and request.method == 'POST' and 'save' in request.POST:
        destination = Destination.objects.get(id=request.POST['destination_id'])
        current_user = request.user
        SavedDestination.objects.create(user=current_user, destination=destination)
        return redirect('home')

    if request.user.is_authenticated and request.method == 'POST' and 'delete' in request.POST:
        current_user = request.user
        destination = Destination.objects.get(id=request.POST['destination_id'])
        saved_destination = SavedDestination.objects.get(user=current_user, destination=destination)
        saved_destination.delete()
        return redirect('home')

    return render(request, 'destinations/list.html', context)


def details(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)
    search_form = DestinationSearchForm()
    booking_form = BookingForm()

    context = {
        'destination': destination,
        'search_form': search_form,
        'booking_form': booking_form
    }

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.guest = request.user
            booking.destination = destination
            booking.save()

            # Redirect to the booking page with the booking_id
            return redirect('book', destination_id=destination_id, destination_name=destination_name,
                            booking_id=booking.id)

    # Reassign the booking_form after processing the POST request
    context['booking_form'] = booking_form

    return render(request, 'destinations/details.html', context)


def search(request):
    form = DestinationSearchForm(request.GET)
    if form.is_valid():
        city = form.cleaned_data['city']
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']
        guests = form.cleaned_data['guests']

        # Perform search based on form data
        # For example:
        results = Destination.objects.filter(city=city)

        return render(request, 'destinations/search.html', {'results': results})
    else:
        return render(request, 'destinations/search.html', {'results': None})


@login_required
def create(request):
    current_user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        destination_form = DestinationForm(request.POST, request.FILES)
        photo_formset = PhotoFormSet(request.POST, request.FILES)
        if destination_form.is_valid() and photo_formset.is_valid():
            destination = destination_form.save(commit=False)
            destination.host = request.user
            destination.save()
            photo_formset.instance = destination
            photo_formset.save()

            if not current_user.is_host:
                current_user.is_host = True
                current_user.save()

            if 'save' in request.POST:
                return redirect('listings')
            elif 'save-and-add-another' in request.POST:
                return redirect('create_destination')

    else:
        destination_form = DestinationForm()
        photo_formset = PhotoFormSet()
        return render(request, 'destinations/create.html',
                      {'destination_form': destination_form, 'photo_formset': photo_formset})


@login_required
def update(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)

    # Check if the current user is the host of the destination
    if not destination.host == request.user:
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Get the existing photos for the destination
    existing_photos = destination.photos.all()

    if request.method == 'POST':
        destination_form = DestinationForm(request.POST, request.FILES, instance=destination)
        photo_formset = PhotoFormSet(request.POST, request.FILES, instance=destination)

        if destination_form.is_valid() and photo_formset.is_valid():
            destination_form.save()
            photo_formset.save()

            return redirect('listings')
    else:
        destination_form = DestinationForm(instance=destination)
        photo_formset = PhotoFormSet(instance=destination)

    return render(request, 'destinations/update.html', {
        'destination_form': destination_form,
        'photo_formset': photo_formset,
        'destination': destination,
        'existing_photos': existing_photos,  # Pass the existing photos to the template
    })


@login_required
def delete(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)

    if not destination.host == request.user:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        destination.delete()
        return redirect('listings')

    return render(request, 'destinations/delete.html', {'destination': destination})
