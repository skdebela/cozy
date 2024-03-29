from django.contrib import admin
from .models import Structure, Type, Amenity, StandoutAmenity, AccessibilityItem, SafetyConsideration, \
    SafetyDevice, PropertyInformation, CheckoutInstruction, Photo, Destination

# Get all models from the destinations app
models_to_register = [Structure, Type, Amenity, StandoutAmenity, AccessibilityItem, SafetyConsideration,
                      SafetyDevice, PropertyInformation, CheckoutInstruction, Photo, Destination]

# Register each model dynamically
for model in models_to_register:
    admin.site.register(model)
