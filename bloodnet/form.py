from django import forms
from .models import *

class donor_form(forms.ModelForm):
    class Meta:
        model = add_donors
        fields = ['donor_name', 'donor_age', 'donor_contact', 'blood_group']

class blood_form(forms.ModelForm):
    class Meta:
        model = blood_request
        fields = [
            'patient_name',
            'patient_age', 
            'patient_contact',
            'patient_bg',
            'hospital_name',
            'hospital_area',
            'blood_units',
            'last_date',
        ]
        widgets = {
            'last_date': forms.DateInput(attrs={'type': 'date'}),
            'patient_bg': forms.Select(choices=[
                ('', 'Select Blood Group'),
                ('A+', 'A+'), ('A-', 'A-'),
                ('B+', 'B+'), ('B-', 'B-'),
                ('AB+', 'AB+'), ('AB-', 'AB-'),
                ('O+', 'O+'), ('O-', 'O-'),
            ]),
        }