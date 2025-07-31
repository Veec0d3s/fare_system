from django.urls import path
from .views import simulate_tap

urlpatterns = [
    path('simulate/', simulate_tap, name='simulate_tap'),
]
