from django.db import models

# Create your models here.

class add_donors(models.Model):
    donor_name=models.CharField(max_length=100)
    donor_age=models.IntegerField(default=None)
    donor_contact=models.IntegerField(default=None)
    blood_group=models.CharField(max_length=10)

    def __str__(self):
        return(self.donor_name)
