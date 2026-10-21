from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, Event, Registration


class ModelTests(TestCase):
    def setUp(self):
        # organizer
        self.org_user = User.objects.create_user(
            username="org1",
            password="test12345",
            email="org1@cis.edu",
        )
        self.org_profile = UserProfile.objects.create(
            user=self.org_user,
            role=UserProfile.ROLE_ORGANIZER,
            department="CIS",
            phone="03001234567",
        )

        # students
        self.stu1 = User.objects.create_user(username="ali", password="test12345")
        UserProfile.objects.create(
            user=self.stu1,
            role=UserProfile.ROLE_STUDENT,
            student_id="CIS-001",
            department="CIS",
        )

        self.stu2 = User.objects.create_user(username="sara", password="test12345")
        UserProfile.objects.create(
            user=self.stu2,
            role=UserProfile.ROLE_STUDENT,
            student_id="CIS-002",
            department="CIS",
        )

        now = timezone.now()
        self.event = Event.objects.create(
            title="Python Workshop",
            description="Basic python for CIS students",
            venue="Lab 2",
            start_datetime=now + timedelta(days=2),
            end_datetime=now + timedelta(days=2, hours=3),
            capacity=2,
            status=Event.STATUS_UPCOMING,
            organizer=self.org_user,
        )

    def test_profile_is_linked_to_user(self):
        self.assertEqual(self.org_user.profile.role, "organizer")
        self.assertEqual(self.stu1.profile.role, "student")

    def test_event_belongs_to_organizer(self):
        self.assertEqual(self.event.organizer.username, "org1")
        self.assertEqual(self.org_user.organized_events.count(), 1)

    def test_student_can_register(self):
        reg = Registration.objects.create(event=self.event, student=self.stu1)
        self.assertEqual(reg.event.title, "Python Workshop")
        self.assertEqual(self.event.registered_count(), 1)
        self.assertEqual(self.event.seats_left(), 1)

    def test_duplicate_registration_not_allowed(self):
        Registration.objects.create(event=self.event, student=self.stu1)
        with self.assertRaises(ValidationError):
            Registration(event=self.event, student=self.stu1).save()

    def test_duplicate_blocked_by_database_too(self):
        Registration.objects.create(event=self.event, student=self.stu1)
        # skip model.clean() and try to insert directly
        bad = Registration(event=self.event, student=self.stu1)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                super(Registration, bad).save()

    def test_capacity_limit(self):
        Registration.objects.create(event=self.event, student=self.stu1)
        Registration.objects.create(event=self.event, student=self.stu2)
        self.assertTrue(self.event.is_full())

        extra = User.objects.create_user(username="hamza", password="test12345")
        UserProfile.objects.create(user=extra, role=UserProfile.ROLE_STUDENT, student_id="CIS-003")

        with self.assertRaises(ValidationError):
            Registration.objects.create(event=self.event, student=extra)

    def test_organizer_cannot_register(self):
        with self.assertRaises(ValidationError):
            Registration.objects.create(event=self.event, student=self.org_user)

    def test_cancelled_event_no_register(self):
        self.event.status = Event.STATUS_CANCELLED
        self.event.save()
        with self.assertRaises(ValidationError):
            Registration.objects.create(event=self.event, student=self.stu1)
