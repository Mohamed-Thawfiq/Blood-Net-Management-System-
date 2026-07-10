"""
URL configuration for tntj_bw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bloodnet.views import PublicDonorCreateView
from authentication.views import loginpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('donor/', include('bloodnet.urls')),
    path('public-donor/submit/', PublicDonorCreateView.as_view()),
    path('', loginpage.as_view(), name='login'),
    path('', include('authentication.urls')),
]
