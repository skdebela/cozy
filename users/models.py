from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User Model"""
    
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = (MALE, 'Male', FEMALE, 'Female')

    USD = 'usd'
    ETB = 'etb'

    CURRENCY_CHOICES = (USD, 'usd', ETB, 'etb')

    avatar = models.ImageField(upload_to='', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, blank=True, default=ETB)
    is_host = models.BooleanField(default=False)


