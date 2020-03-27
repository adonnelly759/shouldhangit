from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Weather.as_view(), name="weather")
]