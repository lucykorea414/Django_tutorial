from django.urls import path, include
from . import views

urlpatterns = [
    path('sociallogin/', include('allauth.urls')),
    path('', views.sociallogin, name='sociallogin'),
]