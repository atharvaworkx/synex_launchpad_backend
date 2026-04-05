"""
Views for handling contact form submissions with email integration
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from .email_service import ContactEmailService


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_form(request):
    """
    Handle contact form submission and send email
    
    POST /api/contact/submit/
    
    Expected payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "company": "Acme Corp",
        "message": "I'm interested in your services..."
    }
    
    Returns:
    {
        "success": true,
        "message": "Thank you for your submission",
        "data": {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "company": "Acme Corp",
            "message": "I'm interested in your services...",
            "created_at": "2024-04-05T10:30:00Z"
        }
    }
    """
    if request.method == 'POST':
        # Validate and save the contact submission
        serializer = ContactSubmissionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save to database
            contact = serializer.save()
            
            # Prepare email data
            email_data = {
                'name': contact.name,
                'email': contact.email,
                'company': contact.company,
                'message': contact.message,
            }
            
            # Send email to company
            company_email_sent = ContactEmailService.send_contact_email(email_data)
            
            # Send confirmation email to customer
            customer_email_sent = ContactEmailService.send_confirmation_email(
                contact.email,
                contact.name
            )
            
            response_data = {
                'success': True,
                'message': 'Thank you for your submission. We will respond within 24 hours.',
                'data': serializer.data,
                'email_status': {
                    'company_email_sent': company_email_sent,
                    'customer_confirmation_sent': customer_email_sent,
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'success': False,
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Method not allowed'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def contact_submissions_list(request):
    """
    List all contact submissions (admin only)
    GET /api/contact/submissions/
    """
    submissions = ContactSubmission.objects.all()
    serializer = ContactSubmissionSerializer(submissions, many=True)
    return Response({
        'success': True,
        'count': submissions.count(),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def contact_submission_detail(request, pk):
    """
    Get a specific contact submission
    GET /api/contact/submissions/<id>/
    """
    try:
        contact = ContactSubmission.objects.get(pk=pk)
        serializer = ContactSubmissionSerializer(contact)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except ContactSubmission.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Contact submission not found'
        }, status=status.HTTP_404_NOT_FOUND)
