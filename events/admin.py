from django.contrib import admin
from .models import UserProfile, Event, Registration


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "student_id", "department", "phone"]
    list_filter = ["role", "department"]
    search_fields = ["user__username", "student_id"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "venue", "start_datetime", "capacity", "status", "organizer"]
    list_filter = ["status"]
    search_fields = ["title", "venue"]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["student", "event", "registered_at"]
    list_filter = ["event"]
    search_fields = ["student__username", "event__title"]
