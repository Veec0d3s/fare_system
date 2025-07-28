# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TransportMode(models.Model):
    name = models.CharField(max_length=50)  # e.g., Bus, Train

    def __str__(self):
        return self.name

from django.utils import timezone
from datetime import timedelta

class FareSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    last_tap_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def is_within_session(self):
        return timezone.now() - self.last_tap_at <= timedelta(minutes=30)

class TapEvent(models.Model):
    TAP_TYPES = (("IN", "Tap In"), ("OUT", "Tap Out"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fare_session = models.ForeignKey(FareSession, on_delete=models.SET_NULL, null=True, blank=True)
    transport_mode = models.ForeignKey(TransportMode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    tap_type = models.CharField(max_length=3, choices=TAP_TYPES)
    location = models.CharField(max_length=100)  # Optional: Stop or station name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fare_session = models.ForeignKey(FareSession, on_delete=models.CASCADE)
    amount_charged = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
