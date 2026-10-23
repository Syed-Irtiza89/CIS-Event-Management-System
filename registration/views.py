from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from events.models import Event


def event_list(request):
    events = Event.objects.filter(status="upcoming", start_datetime__gt=timezone.now())
    lines = [f"{e.id}: {e.title} - {e.seats_left()} seats left" for e in events]
    return HttpResponse("\n".join(lines) or "No upcoming events", content_type="text/plain")