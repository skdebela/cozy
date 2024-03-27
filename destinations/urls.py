from django.urls import path
from destinations import views as destinations_views

urlpatterns = [
    path('', destinations_views.home_view, name='home'),
    path('destinations/<int:destination_id>/<slug:destination_name>', destinations_views.details, name='details'),
    path('hosting/create-destination/', destinations_views.create, name='create_destination'),
    path('hosting/destinations/<int:destination_id>/<slug:destination_name>/update', destinations_views.update,
         name='update_destination'),
    path('hosting/destinations/<int:destination_id>/<slug:destination_name>/delete', destinations_views.delete,
         name='delete_destination'),
]
