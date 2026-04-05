"""
Email service for sending contact form submissions via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ContactEmailService:
    """Service to handle sending contact form emails"""

    @staticmethod
    def send_contact_email(contact_data):
        """Send contact form details via email to the company email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"New Contact Submission from {contact_data['name']}"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = settings.CONTACT_EMAIL_TO
            msg['Reply-To'] = contact_data['email']
            
            # Plain text version
            text = f"""
New Contact Form Submission

Name: {contact_data['name']}
Email: {contact_data['email']}
Company: {contact_data.get('company', 'Not provided')}

Message:
{contact_data['message']}

---
Reply to: {contact_data['email']}
            """
            
            # HTML version
            html = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #0066cc;">New Contact Form Submission</h2>
    <p><strong>Name:</strong> {contact_data['name']}</p>
    <p><strong>Email:</strong> <a href="mailto:{contact_data['email']}">{contact_data['email']}</a></p>
    <p><strong>Company:</strong> {contact_data.get('company', 'Not provided')}</p>
    <p><strong>Message:</strong></p>
    <p style="background: #f5f5f5; padding: 15px; border-left: 3px solid #0066cc;">
        {contact_data['message']}
    </p>
</body>
</html>
            """
            
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send via SMTP
            logger.info(f"Connecting to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30)
            server.set_debuglevel(1)  # Enable debug output
            server.ehlo()
            server.starttls()
            server.ehlo()
            
            logger.info(f"Logging in as {settings.EMAIL_HOST_USER}")
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            logger.info(f"Sending email to {settings.CONTACT_EMAIL_TO}")
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {settings.CONTACT_EMAIL_TO}")
            return True
            
        except Exception as e:
            import traceback
            logger.error(f"Error sending email: {str(e)}")
            logger.error(traceback.format_exc())
            return False

    @staticmethod
    def send_confirmation_email(customer_email, customer_name):
        """Send confirmation email to the customer"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "We received your message - Synex Innovations"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = customer_email
            
            # Plain text version
            text = f"""
Hi {customer_name},

Thank you for contacting Synex Innovations!

We've received your message and will respond within 24 hours.

Best regards,
Synex Innovations Team
            """
            
            # HTML version
            html = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #0066cc;">Thank You for Reaching Out!</h2>
    <p>Hi {customer_name},</p>
    <p>We've received your message and will respond within 24 hours.</p>
    <p>Best regards,<br><strong>Synex Innovations Team</strong></p>
</body>
</html>
            """
            
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send via SMTP
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Confirmation email sent to {customer_email}")
            return True
            
        except Exception as e:
            import traceback
            logger.error(f"Error sending confirmation: {str(e)}")
            logger.error(traceback.format_exc())
            return False
