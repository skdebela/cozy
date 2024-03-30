from decimal import Decimal

from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from core.models import AbstractTimeStamp
from django.core.exceptions import ValidationError


class Booking(AbstractTimeStamp):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled')
    ]

    guest = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='bookings', null=True)
    destination = models.ForeignKey(to='destinations.Destination', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', verbose_name='Status')
    check_in = models.DateField()
    check_out = models.DateField()

    def clean(self):
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after the check-in date.")

    def __str__(self):
        return f'{self.guest} books {self.destination.name}: {self.check_in} - {self.check_out}'

    @property
    def nights(self):
        nights = (self.check_out - self.check_in).days
        return nights

    @property
    def sub_total(self):
        """  Calculate the total price based on duration of stay.
        """

        sub_total = self.destination.nightly_price * self.nights
        return sub_total.quantize(Decimal('0.00'))

    @property
    def total_price(self):
        total_price = self.sub_total
        num_bookings = Booking.objects.filter(destination=self.destination).count()
        new_listing = num_bookings <= 3

        # Apply new listing promotion discount for first 3 bookings
        if self.destination.new_listing_promotion and new_listing:
            total_price *= Decimal(0.8) # 20% discount

        # Apply weekly discount
        if self.nights in range(7, 28) and self.destination.weekly_discount_percentage is not None:
            total_price *= (1 - Decimal(self.destination.weekly_discount_percentage / 100))

        # Apply monthly discount
        if self.nights >= 28 and self.destination.monthly_discount_percentage is not None:
            total_price *= (1 - Decimal(self.destination.monthly_discount_percentage / 100))

        # Add cleaning fee
        if self.destination.cleaning_fee:
            total_price += self.destination.cleaning_fee

        return total_price.quantize(Decimal('0.00'))

    @property
    def earning_after_commission(self):
        after_commission = self.total_price * Decimal(0.8)
        return after_commission.quantize(Decimal('0.00'))

    def in_progress(self):
        now = timezone.now().date()

        return self.check_in <= now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()

        return now > self.check_out

    is_finished.boolean = True

    def is_upcoming(self):
        now = timezone.now().date()

        return now < self.check_in

    is_upcoming.boolean = True
