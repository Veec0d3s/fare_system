from django.urls import path
from .views import simulate_tap
from .views import simulate_view
from . import views


urlpatterns = [
    path('simulate/', views.simulate_view, name='simulate'),
    path("simulate-tap/<str:card_id>/<str:stage_name>/<str:tap_type>/", simulate_tap, name="simulate_tap"),
    path('simulate/', simulate_view, name='simulate_view'),

]


