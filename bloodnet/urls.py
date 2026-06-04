from django.urls import path
from .views import *

urlpatterns = [
    path('add/',donor_add),
    path('view/',Donor_view),
    path('delete/<int:id>/',donor_delete,name='donor_delete'),
    path('update/<int:id>/',donor_update,name='donor_update'),
]