from decimal import Decimal
from django.db import models
from core.models import AbstractTimeStamp
from users.models import User
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator


class Destination(AbstractTimeStamp):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

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

    structure = models.CharField(max_length=50, choices=STRUCTURE_CHOICES)

    TYPE_CHOICES = [
        ('An entire place', 'An entire place'),
        ('A room', 'A room'),
        ('A shared room', 'A shared room'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # address
    street_address = models.CharField(max_length=255)
    apt_floor_bldg = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    province_state_territory = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    google_calendar_locator = models.CharField(max_length=255, unique=True, blank=True, null=True)

    # Floor plan
    bedrooms = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    beds = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    bathrooms = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)

    AMENITIES_CHOICES = [
        ('Wifi', 'Wifi'),
        ('TV', 'TV'),
        ('Kitchen', 'Kitchen'),
        ('Washer', 'Washer'),
        ('Free parking on premises', 'Free parking on premises'),
        ('Paid parking on premises', 'Paid parking on premises'),
        ('Air conditioning', 'Air conditioning'),
        ('Dedicated workspace', 'Dedicated workspace'),
    ]

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

    SAFETY_ITEMS_CHOICES = [
        ('Smoke alarm', 'Smoke alarm'),
        ('First aid kit', 'First aid kit'),
        ('Fire extinguisher', 'Fire extinguisher'),
        ('Carbon monoxide alarm', 'Carbon monoxide alarm'),
    ]

    ACCESSIBILITY_ITEMS_CHOICES = [
        ('Accessible parking spot', 'Accessible parking spot'),
        ('Lit path to guest entrance', 'Lit path to guest entrance'),
        ('Step free guest entrance', 'Step free guest entrance'),
        ('Guest entrance wider than 32 inches', 'Guest entrance wider than 32 inches'),
        ('Swimming pool or hot tub hoist', 'Swimming pool or hot hoist'),
        ('Ceiling or mobile hoist', 'Ceiling or mobile hoist'),
    ]

    amenities = MultiSelectField(choices=AMENITIES_CHOICES, blank=True, null=True)
    standout_amenities = MultiSelectField(choices=STANDOUT_AMENITIES_CHOICES, blank=True, null=True)
    safety_items = MultiSelectField(choices=SAFETY_ITEMS_CHOICES, blank=True, null=True)
    accessibility_items = MultiSelectField(choices=ACCESSIBILITY_ITEMS_CHOICES, blank=True, null=True)

    # fees in etb
    nightly_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_listing_promotion = models.BooleanField(default=False)
    weekly_discount_percentage = models.IntegerField(null=True, blank=True,
                                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    monthly_discount_percentage = models.IntegerField(null=True, blank=True,
                                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # House rules
    pets_allowed = models.BooleanField(default=False)
    events_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    quiet_hours = models.BooleanField(default=False)
    commercial_photography_allowed = models.BooleanField(default=False)
    guests = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    check_in_start_time = models.TimeField()
    check_in_end_time = models.TimeField()
    check_out_time = models.TimeField()
    additional_rules = models.TextField(blank=True, null=True)

    # safety

    # Safety considerations
    SAFETY_CONSIDERATIONS_CHOICES = [
        ('Not good for children', 'Not a good fit for children 2 – 12'),
        ('Not good for infants', 'Not a good fit for infants under 2'),
        ('No pool or hot tub gate or lock', 'Pool or hot tub doesn’t have a gate or lock'),
        ('Nearby water', 'Nearby water, like a lake or river'),
        ('Climbing or play structure on destination', 'Climbing or play structure(s) on the property'),
        ('There are Heights without rails or protection', 'There are heights without rails or protection'),
        ('Potentially dangerous animal on destination', 'Potentially dangerous animal(s) on the property'),
    ]

    safety_considerations = MultiSelectField(choices=SAFETY_CONSIDERATIONS_CHOICES, blank=True, null=True)

    # Safety devices
    SAFETY_DEVICES_CHOICES = [
        ('Carbon monoxide alarm', 'Carbon monoxide alarm'),
        ('Smoke alarm', 'Smoke alarm')
    ]
    safety_devices = MultiSelectField(choices=SAFETY_DEVICES_CHOICES, blank=True, null=True)

    # Property information
    PROPERTY_INFORMATION_CHOICES = [
        ('Must climb stairs', 'Must climb stairs'),
        ('Potential noise during stays', 'Potential noise during stays'),
        ('Pets live on property', 'Pets live on property'),
        ('No parking on property', 'No parking on property'),
        ('Shared spaces', 'Shared spaces'),
    ]

    property_information = MultiSelectField(choices=PROPERTY_INFORMATION_CHOICES, blank=True, null=True)

    # Cancellation policy
    CANCELLATION_POLICY_CHOICES = [
        ('Flexible', 'Flexible'),
        ('Moderate', 'Moderate'),
        ('Firm', 'Firm'),
        ('Strict', 'Strict'),
        ('Non-refundable', 'Non-refundable'),
    ]
    cancellation_policy = models.CharField(
        max_length=15,
        choices=CANCELLATION_POLICY_CHOICES,
        default='flexible'
    )

    directions = models.TextField(null=True, blank=True)

    # Check-in method
    CHECK_IN_METHOD_CHOICES = [
        ('Smart lock', 'Smart lock'),
        ('Keypad', 'Keypad'),
        ('Lockbox', 'Lockbox'),
        ('Building staff', 'Building staff'),
        ('In-person greeting', 'In-person greeting'),
        ('Other', 'Other'),
    ]
    check_in_method = models.CharField(
        max_length=20,
        choices=CHECK_IN_METHOD_CHOICES,
        default='in_person_greeting'
    )
    other_check_in_method = models.TextField(null=True, blank=True)

    # WiFi details
    wifi_network_name = models.CharField(max_length=100, blank=True, null=True)
    wifi_password = models.CharField(max_length=100, blank=True, null=True)

    # House manual
    house_manual = models.TextField(blank=True, null=True)

    # checkouts
    CHECKOUT_INSTRUCTIONS_CHOICES = [
        ('Gather towels', 'Gather used towels'),
        ('Throw trash', 'Throw trash away'),
        ('Turn off', 'Turn things off'),
        ('Lock up', 'Lock up'),
        ('Return keys', 'Return keys'),
    ]

    checkout_instructions = MultiSelectField(choices=CHECKOUT_INSTRUCTIONS_CHOICES, null=True, blank=True)
    additional_requests = models.TextField(blank=True, null=True)

    instant_book = models.BooleanField(default=True)
    host = models.ForeignKey(User, related_name="destinations", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_total_cost(self, nights=1):
        """
        Calculate the total price based on duration of stay.
        """

        total_price = 0

        # Apply nightly price
        total_price += self.nightly_price * nights

        # Apply new listing promotion discount for first 3 bookings
        if self.new_listing_promotion:  # and is first 3 booking
            # total_price *= 0.8  # 20% discount
            pass

        # Apply weekly discount
        if nights in range(7, 28) and self.weekly_discount_percentage is not None:
            total_price *= (1 - Decimal(self.weekly_discount_percentage / 100))

        # Apply monthly discount
        if nights >= 28 and self.monthly_discount_percentage is not None:
            total_price *= (1 - Decimal(self.monthly_discount_percentage / 100))

        # Add cleaning fee
        if self.cleaning_fee:
            total_price += self.cleaning_fee

        return total_price

    @property
    def first_photo(self):
        """
        Returns the first photo associated with the destination.
        """
        return self.photos.first()

    @property
    def next_four_photos(self):
        """
        Returns the next four photos associated with the destination.
        """
        return self.photos.all()[1:5]


class Photo(AbstractTimeStamp):
    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to='')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='photos')

