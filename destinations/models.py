from decimal import Decimal
from django.db import models
from core.models import AbstractTimeStamp
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class AbstractItems(AbstractTimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Structure(AbstractItems):
    pass


class Type(AbstractItems):
    pass


class Amenity(AbstractItems):
    class Meta:
        verbose_name_plural = "Amenities"


class StandoutAmenity(AbstractItems):
    class Meta:
        verbose_name = "Standout Amenity"
        verbose_name_plural = "Standout Amenities"


class AccessibilityItem(AbstractItems):
    class Meta:
        verbose_name = "Accessibility Item"
        verbose_name_plural = "Accessibility Items"


class SafetyConsideration(AbstractItems):
    class Meta:
        verbose_name = "Safety Consideration"
        verbose_name_plural = "Safety Considerations"


class SafetyDevice(AbstractItems):
    class Meta:
        verbose_name = "Safety Device"
        verbose_name_plural = "Safety Devices"


class PropertyInformation(AbstractItems):
    class Meta:
        verbose_name = "Property Information"
        verbose_name_plural = "Property Information"


class CheckoutInstruction(AbstractItems):
    class Meta:
        verbose_name = "Checkout Instruction"
        verbose_name_plural = "Checkout Instructions"


class Photo(AbstractTimeStamp):
    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to='')
    destination = models.ForeignKey(to='destinations.Destination', on_delete=models.CASCADE, related_name='photos')


class Destination(AbstractItems):
    CANCELLATION_POLICY_CHOICES = [
        ('Flexible', 'Flexible'),
        ('Moderate', 'Moderate'),
        ('Firm', 'Firm'),
        ('Strict', 'Strict'),
        ('Non-refundable', 'Non-refundable'),
    ]

    CHECK_IN_METHOD_CHOICES = [
        ('Smart lock', 'Smart lock'),
        ('Keypad', 'Keypad'),
        ('Lockbox', 'Lockbox'),
        ('Building staff', 'Building staff'),
        ('In-person greeting', 'In-person greeting'),
        ('Other', 'Other'),
    ]

    description = models.TextField()
    host = models.ForeignKey(User, limit_choices_to={'is_host': True}, related_name="destinations",
                             on_delete=models.CASCADE)
    instant_book = models.BooleanField(default=True)

    # property
    structure = models.ForeignKey(to='destinations.Structure', on_delete=models.CASCADE)
    type = models.ForeignKey(to='destinations.Type', on_delete=models.CASCADE)
    amenities = models.ManyToManyField(to='destinations.Amenity')
    standout_amenities = models.ManyToManyField(to='destinations.StandoutAmenity')
    accessibility_items = models.ManyToManyField(to='destinations.AccessibilityItem')
    wifi_network_name = models.CharField(max_length=100, blank=True, null=True)
    wifi_password = models.CharField(max_length=100, blank=True, null=True)
    house_manual = models.TextField(blank=True, null=True)

    # Floor plan
    bedrooms = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    beds = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    bathrooms = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)

    # House rules
    guests = models.IntegerField(choices=[(i, i) for i in range(1, 12)], default=1)
    pets_allowed = models.BooleanField(default=False)
    events_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    commercial_photography_allowed = models.BooleanField(default=False)
    check_in_start_time = models.TimeField()
    check_in_end_time = models.TimeField()
    check_out_time = models.TimeField()
    additional_rules = models.TextField(blank=True, null=True)

    # fees in etb
    nightly_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_listing_promotion = models.BooleanField(default=False)
    weekly_discount_percentage = models.IntegerField(null=True, blank=True,
                                                     validators=[MinValueValidator(0), MaxValueValidator(50)])
    monthly_discount_percentage = models.IntegerField(null=True, blank=True,
                                                      validators=[MinValueValidator(0), MaxValueValidator(50)])
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # address
    street_address = models.CharField(max_length=255)
    apt_floor_bldg = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    province_state_territory = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    google_calendar_locator = models.CharField(max_length=255, unique=True, blank=True, null=True)
    directions = models.TextField(null=True, blank=True)

    # safety
    safety_considerations = models.ManyToManyField(to='destinations.SafetyConsideration')
    safety_devices = models.ManyToManyField(to='destinations.SafetyDevice')
    property_information = models.ManyToManyField(to='destinations.PropertyInformation')

    # Check-in method
    check_in_method = models.CharField(max_length=50, choices=CHECK_IN_METHOD_CHOICES, default='in_person_greeting',
                                       null=True, blank=True)
    other_check_in_method = models.TextField(null=True, blank=True)

    # checkouts
    checkout_instructions = models.ManyToManyField(to='destinations.CheckoutInstruction')
    additional_checkout_instructions = models.TextField(blank=True, null=True)

    # Cancellation policy
    cancellation_policy = models.CharField(max_length=50, choices=CANCELLATION_POLICY_CHOICES, default='flexible',
                                           null=True, blank=True)

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
