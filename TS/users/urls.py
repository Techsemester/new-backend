from django.urls import path, include
from . import views

app_name='users'

urlpatterns=[
    path('', views.home, name='home'),
]