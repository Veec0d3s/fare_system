from django.urls import path
from .views import simulate_tap

urlpatterns = [
    path("simulate-tap/<str:card_id>/<str:stage_name>/<str:tap_type>/", simulate_tap, name="simulate_tap"),
]


