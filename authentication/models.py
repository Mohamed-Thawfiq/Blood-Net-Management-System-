from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id_num = models.CharField(max_length=50, default='', blank=True)
    area = models.CharField(max_length=100, default='', blank=True)
    contact = models.CharField(max_length=20, default='', blank=True)

    role_choice = (
        (1, 'Manager'),
        (2, 'Area Manager'),
    )
    role = models.IntegerField(default=2, choices=role_choice)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"