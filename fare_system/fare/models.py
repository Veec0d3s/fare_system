# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class TransportMode(models.Model):
    name = models.CharField(max_length=50)  # e.g., Bus, Train

    def __str__(self):
        return self.name
class Passenger(models.Model):
    card_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.card_id
    
class FareSession(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    tap_in_time = models.DateTimeField(default=timezone.now)
    tap_out_time = models.DateTimeField(null=True, blank=True)
    fare_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    entry_stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, related_name='entry_sessions')
    exit_stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True, related_name='exit_sessions')

    def is_active(self):
        return self.tap_out_time is None

    def __str__(self):
        return f"{self.passenger.card_id} - {'Active' if self.is_active() else 'Complete'}"

class Stage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fare_zone = models.IntegerField()  # e.g. 1, 2, 3, 4

    def __str__(self):
        return self.name
class TapEvent(models.Model):
    TAP_TYPES = (("IN", "Tap In"), ("OUT", "Tap Out"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fare_session = models.ForeignKey(FareSession, on_delete=models.SET_NULL, null=True, blank=True)
    transport_mode = models.ForeignKey(TransportMode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    tap_type = models.CharField(max_length=3, choices=TAP_TYPES)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)  # ✅ Replace location field


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fare_session = models.ForeignKey(FareSession, on_delete=models.CASCADE)
    amount_charged = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


