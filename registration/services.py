from django.core.exceptions import ValidationError
from django.utils import timezone
from events.models import Registration


def register_for_event(user, event):
    # rule the models don't cover: event already started
    if event.start_datetime <= timezone.now():
        raise ValidationError("This event has already started.")

    registration = Registration(event=event, student=user)
    registration.save()  # runs the model checks: cancelled/completed, full, duplicate, student-only
    return registration


def cancel_registration(user, event):
    deleted, _ = Registration.objects.filter(event=event, student=user).delete()
    if not deleted:
        raise ValidationError("You are not registered for this event.")