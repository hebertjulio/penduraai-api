from django.urls import path

from .consumers import TokenConsumer


urlpatterns = [
    path('tokens/<str:key>', TokenConsumer),
]
