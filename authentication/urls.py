from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginpage.as_view(), name='login'),
    path('logout/', logoutuser.as_view()),
    path('register/', registerpage.as_view()),
    path('dashboard/manager/', ManagerDashboard.as_view(), name='manager_dashboard'),
    path('dashboard/area/', AreaManagerDashboard.as_view(), name='area_dashboard'),
]