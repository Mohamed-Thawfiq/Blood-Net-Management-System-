from django.urls import path
from .views import *

urlpatterns = [
    path('public-donor/submit/', PublicDonorCreateView.as_view(), name='public_donor_submit'),
    path('add/', adding_donor.as_view()),
    path('view/', donor_view.as_view()),
    path('delete/<int:id>/', donor_delete.as_view(), name='donor_delete'),
    path('update/<int:id>/', donor_update.as_view(), name='donor_update'),
    path('addrequest/', blood_requests.as_view()),
    path('bloodreq/', viewreq.as_view()),
    path('request/<int:id>/action/', request_action.as_view(), name='blood_request_action'),
    path('donations/', donation_history_view.as_view(), name='donation_history'),
    path('appoint/', appoint_donor.as_view(), name='appoint_donor'),
    path('appoint/<int:id>/call/', call_appointment_process.as_view(), name='call_appointment'),
    path('temporary-rejection/', temporary_rejection_view.as_view(), name='temp_rejection'),
    path('permanent-rejection/', permanent_rejection_view.as_view(), name='perm_rejection'),
    path('permanent-rejection/<int:id>/delete/', permanent_rejection_view.as_view(), name='perm_rejection_delete'),
    path('appointed/', appointed_donor_view.as_view(), name='appointed_donors'),
    path('appointed/<int:id>/action/', appointment_action.as_view(), name='appointment_action'),
]