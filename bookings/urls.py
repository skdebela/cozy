from django.urls import path
from bookings import views as bookings_views

urlpatterns = [
    path('booking/<int:destination_id>/<slug:destination_name>/<int:booking_id>', bookings_views.book, name='book'),
    path('booking/<int:booking_id>/success', bookings_views.booking_successful, name='booking_successful'),
    path('booking/approve/<int:booking_id>', bookings_views.approve_booking, name='approve_booking')
]
