from django.db import models
from core.models import AbstractTimeStamp
from users.models import User


class AbstractItem(AbstractTimeStamp):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DestinationType(AbstractItem):
    pass


class Amenity(AbstractItem):
    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    pass


class State(AbstractItem):
    pass


class City(AbstractItem):
    class Meta:
        verbose_name_plural = "Cities"


class Destination(AbstractItem):
    description = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=140)
    guests_capacity = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        User, related_name="destinations", on_delete=models.CASCADE
    )
    destination_type = models.ForeignKey(
        DestinationType, related_name="destinations", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="destinations", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="destinations", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="destinations", blank=True)

    # fees in etb
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    weekly_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True)

    def get_total_cost(self, duration=1):
        """
        calculate the total price based on duration of stay.
        """

        total_price = 0

        if duration in range(7):
            total_price += self.daily_price * duration
        elif duration in range(7, 30):
            total_price += ((self.daily_price * duration) - (self.weekly_discount * (duration / 7)))
        elif duration >= 30:
            total_price += ((self.daily_price * duration) - (self.monthly_discount * (duration / 30)))

        total_price += self.cleaning_fee

        return total_price


class Photo(AbstractTimeStamp):
    caption = models.CharField(max_length=100)
    file = models.ImageField(upload_to='')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='photos')

