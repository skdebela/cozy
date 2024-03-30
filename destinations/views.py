from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from bookings.forms import BookingForm
from bookings.models import Booking
from destinations.models import Destination
from destinations.forms import DestinationSearchForm, DestinationForm, PhotoFormSet
from users.models import User, SavedDestination
from reviews.models import Review
from reviews.forms import ReviewForm


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
    reviews = Review.objects.filter(destination=destination)
    # user_review = Review.objects.get(user=request.user, destination=destination)
    review_form = ReviewForm()

    context = {
        'destination': destination,
        'search_form': search_form,
        'booking_form': booking_form,
        'reviews': reviews,
        # 'user_review': user_review,
        'review_form': review_form,
    }

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.destination = destination
            booking.save()

            # Redirect to the booking page with the booking_id
            return redirect('book', destination_id=destination_id, destination_name=destination_name,
                            booking_id=booking.id)

    # Reassign the booking_form after processing the POST request
    context['booking_form'] = booking_form

    return render(request, 'destinations/details.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        search_results = Destination.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(street_address__icontains=query) |
            Q(province_state_territory__icontains=query) |
            Q(structure__name__icontains=query) |
            Q(amenities__name__icontains=query) |
            Q(standout_amenities__name__icontains=query)
        ).distinct()
    else:
        search_results = None
    return render(request, 'destinations/search.html', {'search_results': search_results})


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
