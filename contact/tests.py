from django.test import TestCase
from .models import ContactSubmission


class ContactSubmissionTestCase(TestCase):
    def setUp(self):
        ContactSubmission.objects.create(
            name="Test User",
            email="test@example.com",
            company="Test Company",
            message="This is a test message"
        )

    def test_contact_submission_created(self):
        submission = ContactSubmission.objects.get(name="Test User")
        self.assertEqual(submission.email, "test@example.com")
