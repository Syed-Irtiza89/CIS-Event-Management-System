from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from events.models import UserProfile, Event, Registration


class Command(BaseCommand):
    help = "Load sample users, events and registrations"

    def handle(self, *args, **options):
        # organizer accounts
        org1, created = User.objects.get_or_create(
            username="organizer1",
            defaults={
                "email": "organizer1@cis.edu",
                "first_name": "Ahmed",
                "last_name": "Khan",
            },
        )
        if created:
            org1.set_password("password123")
            org1.save()

        org2, created = User.objects.get_or_create(
            username="organizer2",
            defaults={
                "email": "organizer2@cis.edu",
                "first_name": "Fatima",
                "last_name": "Ali",
            },
        )
        if created:
            org2.set_password("password123")
            org2.save()

        UserProfile.objects.get_or_create(
            user=org1,
            defaults={"role": UserProfile.ROLE_ORGANIZER, "department": "CIS", "phone": "03001111111"},
        )
        UserProfile.objects.get_or_create(
            user=org2,
            defaults={"role": UserProfile.ROLE_ORGANIZER, "department": "Software", "phone": "03002222222"},
        )

        # student accounts
        students_info = [
            ("ali", "Ali", "Raza", "CIS-101", "CIS", "03003333333"),
            ("sara", "Sara", "Ahmed", "CIS-102", "CIS", "03004444444"),
            ("hamza", "Hamza", "Malik", "CIS-103", "IT", "03005555555"),
            ("ayesha", "Ayesha", "Noor", "CIS-104", "Software", "03006666666"),
        ]

        student_users = []
        for username, first, last, sid, dept, phone in students_info:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": username + "@student.cis.edu", "first_name": first, "last_name": last},
            )
            if created:
                user.set_password("password123")
                user.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "role": UserProfile.ROLE_STUDENT,
                    "student_id": sid,
                    "department": dept,
                    "phone": phone,
                },
            )
            student_users.append(user)

        now = timezone.now()

        event1, _ = Event.objects.get_or_create(
            title="CIS Orientation",
            defaults={
                "description": "Welcome session for new CIS students.",
                "venue": "Auditorium A",
                "start_datetime": now + timedelta(days=5),
                "end_datetime": now + timedelta(days=5, hours=2),
                "capacity": 50,
                "status": Event.STATUS_UPCOMING,
                "organizer": org1,
            },
        )

        event2, _ = Event.objects.get_or_create(
            title="Django Workshop",
            defaults={
                "description": "Learn Django models and admin panel.",
                "venue": "Computer Lab 3",
                "start_datetime": now + timedelta(days=10),
                "end_datetime": now + timedelta(days=10, hours=4),
                "capacity": 3,
                "status": Event.STATUS_UPCOMING,
                "organizer": org1,
            },
        )

        event3, _ = Event.objects.get_or_create(
            title="Career Seminar",
            defaults={
                "description": "Talk about internships and jobs.",
                "venue": "Seminar Hall",
                "start_datetime": now - timedelta(days=1),
                "end_datetime": now + timedelta(hours=2),
                "capacity": 100,
                "status": Event.STATUS_ONGOING,
                "organizer": org2,
            },
        )

        # registrations (ignore if already added)
        try:
            Registration.objects.get_or_create(event=event1, student=student_users[0])
            Registration.objects.get_or_create(event=event1, student=student_users[1])
            Registration.objects.get_or_create(event=event2, student=student_users[0])
            Registration.objects.get_or_create(event=event2, student=student_users[2])
            Registration.objects.get_or_create(event=event3, student=student_users[3])
        except Exception as e:
            self.stdout.write("Some registrations were skipped: " + str(e))

        self.stdout.write(self.style.SUCCESS("Sample data loaded."))
        self.stdout.write("Login users (password for all = password123):")
        self.stdout.write("  organizer1, organizer2")
        self.stdout.write("  ali, sara, hamza, ayesha")
