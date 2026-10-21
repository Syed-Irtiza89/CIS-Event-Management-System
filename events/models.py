from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# extra details for login users
# Django already has User table for username/password
class UserProfile(models.Model):
    ROLE_STUDENT = "student"
    ROLE_ORGANIZER = "organizer"

    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_ORGANIZER, "Organizer"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username + " (" + self.role + ")"


class Event(models.Model):
    STATUS_UPCOMING = "upcoming"
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_UPCOMING, "Upcoming"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    # max students allowed for this event
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_UPCOMING)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_datetime"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(capacity__gte=1),
                name="event_capacity_at_least_1",
            ),
        ]

    def __str__(self):
        return self.title

    def registered_count(self):
        return self.registrations.count()

    def seats_left(self):
        left = self.capacity - self.registered_count()
        if left < 0:
            return 0
        return left

    def is_full(self):
        if self.registered_count() >= self.capacity:
            return True
        return False

    def clean(self):
        # end time should be after start time
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValidationError("End time should be after start time.")


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # one student can register only one time for the same event
        constraints = [
            models.UniqueConstraint(
                fields=["event", "student"],
                name="unique_student_event_registration",
            ),
        ]

    def __str__(self):
        return self.student.username + " -> " + self.event.title

    def clean(self):
        # some checks before saving (also used by admin form)
        if self.event_id is None:
            return

        event = self.event

        if event.status == Event.STATUS_CANCELLED:
            raise ValidationError("This event is cancelled. Registration is not allowed.")

        if event.status == Event.STATUS_COMPLETED:
            raise ValidationError("This event is already completed.")

        # capacity check (skip current row if we are updating it)
        already = event.registrations.count()
        if self.pk:
            already = event.registrations.exclude(pk=self.pk).count()
        if already >= event.capacity:
            raise ValidationError("Event is full. No seats left.")

        # student should have a student profile
        if self.student_id:
            try:
                profile = self.student.profile
            except UserProfile.DoesNotExist:
                raise ValidationError("This user has no profile.")
            else:
                if profile.role != UserProfile.ROLE_STUDENT:
                    raise ValidationError("Only students can register for events.")

    def save(self, *args, **kwargs):
        # run clean() so bad data is not saved from python code
        self.full_clean()
        super().save(*args, **kwargs)
