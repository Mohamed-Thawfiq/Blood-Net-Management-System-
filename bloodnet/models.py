from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=150, unique=True)
    area_manager = models.OneToOneField(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='managed_area'
    )

    def __str__(self):
        return self.name


class add_donors(models.Model):
    donor_name = models.CharField(max_length=100)
    donor_age = models.IntegerField(default=0)
    donor_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=10)
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    area_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='donors'
    )

    def __str__(self):
        return self.donor_name


class blood_request(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_age = models.IntegerField(default=0)
    patient_contact = models.CharField(max_length=15)
    patient_bg = models.CharField(max_length=10)
    hospital_name = models.CharField(max_length=100)
    hospital_area = models.CharField(max_length=200)
    blood_units = models.IntegerField(default=1)
    last_date = models.DateField(null=True, blank=True)
    requested_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True, related_name='requests_made'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    assigned_area_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='requests_received'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.patient_bg}"


class donation_history(models.Model):
    action_choice = [('donated', 'Donated'), ('dropped', 'Dropped')]
    request = models.ForeignKey(
        blood_request,
        on_delete=models.SET_NULL,
        null=True
    )
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    patient_age = models.CharField(max_length=10, null=True, blank=True)
    patient_contact = models.CharField(max_length=15, null=True, blank=True)
    patient_bg = models.CharField(max_length=10, null=True, blank=True)
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    blood_units = models.IntegerField(null=True, blank=True)
    action = models.CharField(max_length=10, choices=action_choice)
    processed_at = models.DateTimeField(auto_now_add=True)
    area_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='donation_histories'
    )


class donor_appointment(models.Model):
    donor = models.ForeignKey(add_donors, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.donor_name} - {self.patient_name}"


class temporary_rejection(models.Model):
    donor = models.ForeignKey(add_donors, on_delete=models.CASCADE)
    reason = models.TextField()
    available_date = models.DateField()
    rejected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.donor_name} - Temp Rejected"


class permanent_rejection(models.Model):
    donor = models.ForeignKey(add_donors, on_delete=models.CASCADE)
    reason = models.TextField()
    rejected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.donor_name} - Permanently Rejected"


class TerminatedAreaManagerBackup(models.Model):
    """Stores data when an area manager is terminated"""
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    area_name = models.CharField(max_length=150)
    manager_username = models.CharField(max_length=150)
    terminated_at = models.DateTimeField(auto_now_add=True)
    donor_data = models.JSONField(default=list)

    def __str__(self):
        return f"Backup: {self.area_name} - {self.manager_username}"