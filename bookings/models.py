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

    guest = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='bookings')
    destination = models.ForeignKey(to='destinations.Destination', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', verbose_name='Status')
    check_in = models.DateField()
    check_out = models.DateField()

    def clean(self):
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after the check-in date.")

    def __str__(self):
        return f'{self.guest} - {self.destination} on {self.check_in}'

    def in_progress(self):
        now = timezone.now().date()

        return self.check_in <= now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()

        return now > self.check_out

    is_finished.boolean = True
