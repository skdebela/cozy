from django.db import models
from core.models import AbstractTimeStamp


class Review(AbstractTimeStamp):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='reviews')
    destination = models.ForeignKey(to='destinations.Destination', on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    rating = models.FloatField()
