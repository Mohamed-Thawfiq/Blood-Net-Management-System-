from django.urls import path
from .views import *

urlpatterns = [
    path('', loginpage.as_view()),
    path('logout/',logoutuser.as_view()),
    path('register/',registerpage.as_view()),
]