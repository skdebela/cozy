from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from core.models import AbstractTimeStamp

class User(AbstractUser):
    """Custom User Model"""

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('ETB', 'ETB'),
    ]
    
    avatar = models.ImageField(upload_to='', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, blank=True, default='ETB')
    is_host = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username


class SavedDestination(AbstractTimeStamp):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)
    destination = models.ForeignKey(to='destinations.Destination', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} saved {self.destination}'
