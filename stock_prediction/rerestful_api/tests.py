from django.test import TestCase
from django.contrib.auth.models import User
from .models import Reminder
from rest_framework.test import APITestCase
from .serializers import ReminderSerializer, UserSerializer


class ReminderSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.reminder = Reminder.objects.create(
            title="Test Reminder",
            description="This is a test reminder",
            due_date="2024-01-01T15:00:00",
            user=self.user,
        )

    def test_reminder_serialization(self):
        reminder_serializer = ReminderSerializer(instance=self.reminder)
        self.assertEqual(reminder_serializer.data["title"], "Test Reminder")
        self.assertEqual(
            reminder_serializer.data["description"], "This is a test reminder"
        )
        self.assertEqual(reminder_serializer.data["due_date"], "2024-01-01T15:00:00")
        self.assertEqual(reminder_serializer.data["user"], "testuser")


class UserSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.reminder = Reminder.objects.create(
            title="Test Reminder",
            description="This is a test reminder",
            due_date="2024-01-01T15:00:00",
            user=self.user,
        )

    def test_user_serialization(self):
        user_serializer = UserSerializer(instance=self.user)
        self.assertEqual(user_serializer.data["username"], "testuser")
        self.assertEqual(user_serializer.data["email"], "")
        self.assertEqual(len(user_serializer.data["reminders"]), 1)
        self.assertEqual(user_serializer.data["reminders"][0]["title"], "Test Reminder")


class ReminderModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="12345")
        Reminder.objects.create(
            title="Test Reminder",
            description="This is a test reminder",
            due_date="2023-02-20 12:00:00",
            user=user,
        )

    def test_reminder_created(self):
        reminder = Reminder.objects.get(title="Test Reminder")
        self.assertEqual(reminder.description, "This is a test reminder")
        self.assertEqual(
            reminder.due_date.strftime("%Y-%m-%d %H:%M:%S"), "2023-02-20 12:00:00"
        )
        self.assertEqual(reminder.user.username, "testuser")
