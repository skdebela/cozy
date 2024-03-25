from django.core.management.base import BaseCommand
from destinations.models import Structure, Type, Amenity, StandoutAmenity, AccessibilityItem, SafetyConsideration, \
    SafetyDevice, PropertyInformation, CheckoutInstruction

STRUCTURE_CHOICES = [
    ('House', 'House'),
    ('Apartment', 'Apartment'),
    ('Barn', 'Barn'),
    ('Bed & breakfast', 'Bed & breakfast'),
    ('Boat', 'Boat'),
    ('Cabin', 'Cabin'),
    ('Camper/RV', 'Camper/RV'),
    ('Casa particular', 'Casa particular'),
    ('Castle', 'Castle'),
    ('Cave', 'Cave'),
    ('Container', 'Container'),
    ('Cycladic home', 'Cycladic home'),
    ('Dammuso', 'Dammuso'),
    ('Dome', 'Dome'),
    ('Earth home', 'Earth home'),
    ('Farm', 'Farm'),
    ('Guesthouse', 'Guesthouse'),
    ('Hotel', 'Hotel'),
    ('Houseboat', 'Houseboat'),
    ('Kezhan', 'Kezhan'),
    ('Minsu', 'Minsu'),
    ('Riad', 'Riad'),
    ('Ryokan', 'Ryokan'),
    ("Shepherd's hut", "Shepherd's hut"),
    ('Tent', 'Tent'),
    ('Tiny home', 'Tiny home'),
    ('Tower', 'Tower'),
    ('Treehouse', 'Treehouse'),
    ('Trullo', 'Trullo'),
    ('Windmill', 'Windmill'),
    ('Yurt', 'Yurt'),
]

TYPE_CHOICES = [
    ('An entire place', 'An entire place'),
    ('A room', 'A room'),
    ('A shared room', 'A shared room'),
]

AMENITIES_CHOICES = (
    ('Wifi', 'Wifi'),
    ('TV', 'TV'),
    ('Kitchen', 'Kitchen'),
    ('Washer', 'Washer'),
    ('Free parking on premises', 'Free parking on premises'),
    ('Paid parking on premises', 'Paid parking on premises'),
    ('Air conditioning', 'Air conditioning'),
    ('Dedicated workspace', 'Dedicated workspace'),
)

STANDOUT_AMENITIES_CHOICES = [
    ('Pool', 'Pool'),
    ('Hot tub', 'Hot tub'),
    ('Patio', 'Patio'),
    ('BBQ grill', 'BBQ grill'),
    ('Outdoor dining area', 'Outdoor dining area'),
    ('Fire pit', 'Fire pit'),
    ('Pool table', 'Pool table'),
    ('Indoor fireplace', 'Indoor fireplace'),
    ('Piano', 'Piano'),
    ('Exercise equipment', 'Exercise equipment'),
    ('Lake access', 'Lake access'),
    ('Beach access', 'Beach access'),
    ('Ski-in/Ski-out', 'Ski-in/Ski-out'),
    ('Outdoor shower', 'Outdoor shower'),
]

ACCESSIBILITY_ITEMS_CHOICES = [
    ('Accessible parking spot', 'Accessible parking spot'),
    ('Lit path to guest entrance', 'Lit path to guest entrance'),
    ('Step free guest entrance', 'Step free guest entrance'),
    ('Guest entrance wider than 32 inches', 'Guest entrance wider than 32 inches'),
    ('Swimming pool or hot tub hoist', 'Swimming pool or hot hoist'),
    ('Ceiling or mobile hoist', 'Ceiling or mobile hoist'),
]

SAFETY_CONSIDERATIONS_CHOICES = [
    ('Not good for children', 'Not a good fit for children 2 – 12'),
    ('Not good for infants', 'Not a good fit for infants under 2'),
    ('No pool or hot tub gate or lock', 'Pool or hot tub doesn’t have a gate or lock'),
    ('Nearby water', 'Nearby water, like a lake or river'),
    ('Climbing or play structure on destination', 'Climbing or play structure(s) on the property'),
    ('There are Heights without rails or protection', 'There are heights without rails or protection'),
    ('Potentially dangerous animal on destination', 'Potentially dangerous animal(s) on the property'),
]

SAFETY_DEVICES_CHOICES = [
    ('Carbon monoxide alarm', 'Carbon monoxide alarm'),
    ('Smoke alarm', 'Smoke alarm')
]

PROPERTY_INFORMATION_CHOICES = [
    ('Must climb stairs', 'Must climb stairs'),
    ('Potential noise during stays', 'Potential noise during stays'),
    ('Pets live on property', 'Pets live on property'),
    ('No parking on property', 'No parking on property'),
    ('Shared spaces', 'Shared spaces'),
]

CHECKOUT_INSTRUCTIONS_CHOICES = [
    ('Gather towels', 'Gather used towels'),
    ('Throw trash', 'Throw trash away'),
    ('Turn off', 'Turn things off'),
    ('Lock up', 'Lock up'),
    ('Return keys', 'Return keys'),
]


class Command(BaseCommand):
    help = 'Populate the models with initial choices'

    def handle(self, *args, **kwargs):
        self.populate_structure()
        self.populate_type()
        self.populate_amenities()
        self.populate_standout_amenities()
        self.populate_accessibility_items()
        self.populate_safety_considerations()
        self.populate_safety_devices()
        self.populate_property_information()
        self.populate_checkout_instructions()
        self.stdout.write(self.style.SUCCESS('Models populated successfully'))

    def populate_structure(self):
        for choice in STRUCTURE_CHOICES:
            Structure.objects.get_or_create(name=choice[0])

    def populate_type(self):
        for choice in TYPE_CHOICES:
            Type.objects.get_or_create(name=choice[0])

    def populate_amenities(self):
        for choice in AMENITIES_CHOICES:
            Amenity.objects.get_or_create(name=choice[0])

    def populate_standout_amenities(self):
        for choice in STANDOUT_AMENITIES_CHOICES:
            StandoutAmenity.objects.get_or_create(name=choice[0])

    def populate_accessibility_items(self):
        for choice in ACCESSIBILITY_ITEMS_CHOICES:
            AccessibilityItem.objects.get_or_create(name=choice[0])

    def populate_safety_considerations(self):
        for choice in SAFETY_CONSIDERATIONS_CHOICES:
            SafetyConsideration.objects.get_or_create(name=choice[0])

    def populate_safety_devices(self):
        for choice in SAFETY_DEVICES_CHOICES:
            SafetyDevice.objects.get_or_create(name=choice[0])

    def populate_property_information(self):
        for choice in PROPERTY_INFORMATION_CHOICES:
            PropertyInformation.objects.get_or_create(name=choice[0])

    def populate_checkout_instructions(self):
        for choice in CHECKOUT_INSTRUCTIONS_CHOICES:
            CheckoutInstruction.objects.get_or_create(name=choice[0])
