from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'company', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Validate email field"""
        if not value:
            raise serializers.ValidationError("Email is required")
        return value

    def validate_name(self, value):
        """Validate name field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Name is required")
        return value

    def validate_message(self, value):
        """Validate message field"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Message is required")
        return value
