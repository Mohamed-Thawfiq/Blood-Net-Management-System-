from django.forms import ModelForm
from .models import *

class donor_form(ModelForm):
    class Meta:
        model=add_donors
        fields='__all__'