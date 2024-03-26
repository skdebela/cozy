from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import SavedDestination


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def saved(request):
    user = request.user
    saved_destinations = SavedDestination.objects.filter(user=user)

    return render(request, 'users/saved.html', {'saved_destinations': saved_destinations})
