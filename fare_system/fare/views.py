from django.shortcuts import render
from django.utils import timezone
from .models import Passenger, FareSession, TapEvent, Transaction, TransportMode,Stage
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


FARE_BY_ZONE = {
    1: 1000,
    2: 2000,
    3: 3000,
    4: 4000,
}

def simulate_tap(request, card_id, stage_name, tap_type):
    passenger = get_object_or_404(Passenger, card_id=card_id)
    stage = get_object_or_404(Stage, name__iexact=stage_name)

    if tap_type.upper() == "IN":
        FareSession.objects.create(passenger=passenger, entry_stage=stage)
        return HttpResponse(f"{card_id} tapped in at {stage.name}")

    elif tap_type.upper() == "OUT":
        session = FareSession.objects.filter(passenger=passenger, tap_out_time__isnull=True).last()
        if not session:
            return HttpResponse("No active session found.")

        session.tap_out_time = timezone.now()
        session.exit_stage = stage
        session.fare_amount = calculate_fare(session.entry_stage, stage)
        session.save()

        Transaction.objects.create(
            user=request.user,
            fare_session=session,
            amount_charged=session.fare_amount
        )

        return HttpResponse(f"{card_id} tapped out at {stage.name}. Charged UGX {session.fare_amount}")

def calculate_fare(entry_stage, exit_stage):
    zone_difference = abs(entry_stage.fare_zone - exit_stage.fare_zone)

    fare_map = {
        0: 1000,  # Same zone
        1: 1000,
        2: 2000,
        3: 3000,
        4: 4000,
    }

    return fare_map.get(zone_difference, 5000)  # Default if > 4

