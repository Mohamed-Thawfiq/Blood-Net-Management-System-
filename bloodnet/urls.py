from django.urls import path
from .views import *

urlpatterns = [
    path('add/',adding_donor.as_view()),
    path('view/',donor_view.as_view()),
    path('delete/<int:id>/',donor_delete.as_view(),name='donor_delete'),
    path('update/<int:id>/',donor_update.as_view(),name='donor_update'),
]