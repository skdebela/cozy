from django.shortcuts import render
from destinations.models import Destination


def home_view(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations/list.html', {'destinations': destinations})
