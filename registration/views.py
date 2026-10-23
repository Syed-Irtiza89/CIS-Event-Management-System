from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .services import register_for_event
# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from events.models import Event


def event_list(request):
    events = Event.objects.filter(status="upcoming", start_datetime__gt=timezone.now())
    lines = [f"{e.id}: {e.title} - {e.seats_left()} seats left" for e in events]
    return HttpResponse("\n".join(lines) or "No upcoming events", content_type="text/plain")

@login_required
@require_POST
def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        register_for_event(request.user, event)
    except ValidationError as e:
        return HttpResponse(" ".join(e.messages), status=400, content_type="text/plain")
    return HttpResponse("Registered for " + event.title, content_type="text/plain")