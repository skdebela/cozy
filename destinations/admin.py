from django.contrib import admin
from destinations.models import State, City, Destination, DestinationType, Amenity, Facility, HouseRule, Photo


admin.site.register(State)
admin.site.register(City)
admin.site.register(Destination)
admin.site.register(DestinationType)
admin.site.register(Amenity)
admin.site.register(Facility)
admin.site.register(HouseRule)
admin.site.register(Photo)

