from django.contrib import admin
from .models import Passenger, FareSession, TapEvent, Transaction, TransportMode, Stage

admin.site.register(Passenger)
admin.site.register(FareSession)
admin.site.register(TapEvent)
admin.site.register(Transaction)
admin.site.register(TransportMode)
admin.site.register(Stage)
