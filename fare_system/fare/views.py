from django.shortcuts import render
from django.utils import timezone
from .models import Passenger, FareSession, TapEvent, Transaction, TransportMode
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import timedelta

def simulate_tap(request):
    passenger = Passenger.objects.first()  # Simulate the first passenger (for now)
    
    if not passenger:
        return render(request, 'simulate_tap.html', {'message': "No passenger found."})

    active_session = FareSession.objects.filter(passenger=passenger, tap_out_time__isnull=True).first()

    if active_session:
        active_session.tap_out_time = timezone.now()
        active_session.fare_amount = 2000
        active_session.save()
        message = f"{passenger.card_id} tapped OUT."
    else:
        FareSession.objects.create(passenger=passenger)
        message = f"{passenger.card_id} tapped IN."

    return render(request, 'simulate_tap.html', {'message': message})


def calculate_fare(duration):
    # Just an example: flat fee or time-based
    if duration < timedelta(minutes=30):
        return 1000.00  # UGX
    else:
        return 1500.00
