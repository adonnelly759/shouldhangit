from django.urls import path, include
from . import views

app_name = "should"
urlpatterns = [
    path('', views.Weather.as_view(), name="weather"),
]