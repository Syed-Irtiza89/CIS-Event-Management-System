from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.event_list, name="event_list"),
        path("events/<int:event_id>/register/", views.register, name="register"),
]