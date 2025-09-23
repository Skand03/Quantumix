from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.sensor_data, name='sensor_data'),
]
