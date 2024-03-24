from django.urls import path
from destinations import views as destinations_views


urlpatterns = [
    path('', destinations_views.home_view, name='home')
]
