from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from destinations.models import Destination
from destinations.forms import DestinationSearchForm, DestinationForm
from users.models import User


def home_view(request):
    destinations = Destination.objects.all()
    search_form = DestinationSearchForm()

    context = {
        'destinations': destinations,
        'search_form': search_form
    }

    return render(request, 'destinations/list.html', context)


def details(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)

    return render(request, 'destinations/details.html', {'destination': destination})


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
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        user = User.objects.get(username=request.user.username)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.host = request.user
            destination.save()

            if not user.is_host:
                user.is_host = True
                user.save()

            if 'save' in request.POST:
                return redirect('listings')
            elif 'save-and-add-another' in request.POST:
                return redirect('create_destination')

    else:
        form = DestinationForm()
        return render(request, 'destinations/create.html', {'form': form})


@login_required
def update(request, destination_id, destination_name):
    destination = Destination.objects.get(id=destination_id)
    form = DestinationForm(instance=destination)

    if not destination.host.username == request.user.username:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()

        return redirect('listings')

    return render(request, 'destinations/update.html', {'form': form, 'destination': destination})


@login_required
def delete(request, destination_id):
    destination = Destination.objects.get(id=destination_id)

    if not destination.host == request.user:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        destination.delete()
        return redirect('listings')

    return render(request, 'destinations/delete.html', {'destination': destination})
