"""
Email service for sending contact form submissions via SMTP
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class ContactEmailService:
    """Service to handle sending contact form emails"""

    @staticmethod
    def send_contact_email(contact_data):
        """
        Send contact form details via email to the company email

        Args:
            contact_data (dict): Dictionary containing name, email, company, and message

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"New Contact Submission from {contact_data['name']}"
            
            # Email template with HTML formatting
            html_message = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background-color: #0066cc; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                        .header h2 {{ margin: 0; }}
                        .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; }}
                        .field {{ margin-bottom: 20px; }}
                        .label {{ font-weight: bold; color: #0066cc; margin-bottom: 5px; }}
                        .value {{ color: #555; padding: 10px; background-color: white; border-left: 3px solid #0066cc; }}
                        .message-text {{ white-space: pre-wrap; }}
                        .footer {{ margin-top: 20px; font-size: 12px; color: #999; text-align: center; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>New Contact Form Submission</h2>
                        </div>
                        <div class="content">
                            <div class="field">
                                <div class="label">Name:</div>
                                <div class="value">{contact_data['name']}</div>
                            </div>
                            <div class="field">
                                <div class="label">Email:</div>
                                <div class="value"><a href="mailto:{contact_data['email']}">{contact_data['email']}</a></div>
                            </div>
                            <div class="field">
                                <div class="label">Company:</div>
                                <div class="value">{contact_data.get('company', 'Not provided') or 'Not provided'}</div>
                            </div>
                            <div class="field">
                                <div class="label">Message:</div>
                                <div class="value message-text">{contact_data['message']}</div>
                            </div>
                        </div>
                        <div class="footer">
                            <p>This is an automated message from the Synex Innovations contact form.</p>
                            <p>Reply to: {contact_data['email']}</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            plain_message = f"""
            New Contact Form Submission
            
            Name: {contact_data['name']}
            Email: {contact_data['email']}
            Company: {contact_data.get('company', 'Not provided') or 'Not provided'}
            
            Message:
            {contact_data['message']}
            
            ---
            This is an automated message from the Synex Innovations contact form.
            """

            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL_TO],
                html_message=html_message,
                fail_silently=False,
            )

            print(f"Email sent successfully to {settings.CONTACT_EMAIL_TO}")
            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    @staticmethod
    def send_confirmation_email(customer_email, customer_name):
        """
        Send confirmation email to the customer

        Args:
            customer_email (str): Customer's email address
            customer_name (str): Customer's name

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = "We received your message - Synex Innovations"
            
            html_message = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background-color: #0066cc; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                        .header h2 {{ margin: 0; }}
                        .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; }}
                        .btn {{ display: inline-block; margin: 20px 0; padding: 10px 20px; background-color: #0066cc; color: white; text-decoration: none; border-radius: 5px; }}
                        .footer {{ margin-top: 20px; font-size: 12px; color: #999; text-align: center; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>Thank You for Reaching Out!</h2>
                        </div>
                        <div class="content">
                            <p>Hi {customer_name},</p>
                            <p>We've successfully received your contact form submission. We appreciate your interest in Synex Innovations!</p>
                            <p><strong>What's next?</strong></p>
                            <ul>
                                <li>Our team will review your inquiry shortly</li>
                                <li>You can expect a response within 24 hours</li>
                                <li>We'll reach out to the email address you provided: <strong>{customer_email}</strong></li>
                            </ul>
                            <p>If you have any urgent matters, feel free to reach out to us directly at <strong>synexinnovation@gmail.com</strong></p>
                        </div>
                        <div class="footer">
                            <p>© 2024 Synex Innovations. All rights reserved.</p>
                            <p>Pune, Maharashtra, India</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            plain_message = f"""
            Thank You for Reaching Out!
            
            Hi {customer_name},
            
            We've successfully received your contact form submission. We appreciate your interest in Synex Innovations!
            
            What's next?
            - Our team will review your inquiry shortly
            - You can expect a response within 24 hours
            - We'll reach out to the email address you provided: {customer_email}
            
            If you have any urgent matters, feel free to reach out to us directly at synexinnovation@gmail.com
            
            ---
            © 2024 Synex Innovations. All rights reserved.
            """

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                html_message=html_message,
                fail_silently=False,
            )

            print(f"Confirmation email sent to {customer_email}")
            return True

        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
            return False
