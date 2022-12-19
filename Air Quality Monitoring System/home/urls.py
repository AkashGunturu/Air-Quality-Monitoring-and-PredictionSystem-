from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("",views.index,name="home"),
    path("weather",views.weather,name="weather"),
    path("airquality",views.airquality,name="airquality"),
    
]