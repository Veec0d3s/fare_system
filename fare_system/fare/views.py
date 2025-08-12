from django.shortcuts import render
from django.utils import timezone
from .models import Passenger, FareSession, TapEvent, Transaction, TransportMode,Stage
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from .models import Stage  # Import your Stage model
from django.contrib import messages
from django.shortcuts import redirect, render
from datetime import timedelta

FARE_BY_ZONE = {
    0: 0,  # No fare for same zone
    1: 1000,
    2: 2000,
    3: 3000,
    4: 4000,
}

from datetime import timedelta

def simulate_tap(request, card_id, stage_name, tap_type):
    passenger = get_object_or_404(Passenger, card_id=card_id)
    stage = get_object_or_404(Stage, name__iexact=stage_name.strip())

    if tap_type.lower() == "tap_in":
        recent_session = FareSession.objects.filter(
            passenger=passenger,
            tap_out_time__isnull=False
        ).order_by('-tap_out_time').first()

        if recent_session and timezone.now() - recent_session.tap_out_time < timedelta(minutes=30):
            messages.info(request, "Tap-in within 30 mins — no new session started.")
            return redirect('simulate_view')

        FareSession.objects.create(passenger=passenger, entry_stage=stage)
        messages.success(request, f"{card_id} tapped in at {stage.name}")
        return redirect('simulate_view')

def calculate_fare(entry_stage, exit_stage):
    if not entry_stage or not exit_stage:
        return 0  # or raise an exception/log it for debugging

    zone_difference = abs(entry_stage.fare_zone - exit_stage.fare_zone)

    fare_map = {
        0: 0000,
        1: 1000,
        2: 2000,
        3: 3000,
        4: 4000,
    }

    return fare_map.get(zone_difference, 5000)

def simulate_view(request):
    stages = Stage.objects.all()  # Fetch all stages from the database

    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        stage_name = request.POST.get('stage_name')
        tap_type = request.POST.get('tap_type')

        return HttpResponseRedirect(reverse('simulate_tap', args=[card_id, stage_name, tap_type]))

    return render(request, 'simulate_form.html', {'stages': stages})

def tap_out_view(request):
    if request.method == 'POST':
        # Your existing logic here, e.g.:
        session_id = request.POST.get('session_id')
        exit_stage = request.POST.get('exit_stage')
        # Calculate fare
        fare = calculate_fare(session_id, exit_stage)  # your existing function
        
        # Add message
        messages.success(request, f"{session_id} tapped out at {exit_stage}. Fare: UGX {fare}")

        # Redirect back to form page (assuming the URL name is 'tap_out')
        return redirect('tap_out')
    
    # If GET or no POST, just render the form template
    return render(request, 'tap_out_form.html')