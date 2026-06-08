from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class User (AbstractUser):
    name = models.CharField(max_length=150, default='')
    age=models.IntegerField(default=0)
    id_num=models.IntegerField(default=0)
    area=models.TextField(max_length=50)
    contact=models.CharField(max_length=20)

    role_choice = (
        (0, 'Admin'),
        (1, 'District_Manager'),
        (2, 'Area Manager'),
    )
    role = models.IntegerField(default=0, choices=role_choice)