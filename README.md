# Synex Innovations Backend

Django REST Framework backend for contact form submissions with email integration.

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

**Important Email Configuration (Gmail):**
1. Enable 2-Step Verification on your Gmail account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows/Linux" (or your device)
4. Copy the generated 16-character password
5. Update `.env`:
   - `EMAIL_HOST_USER=your-gmail@gmail.com`
   - `EMAIL_HOST_PASSWORD=your-16-character-password`

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## API Endpoints

### Submit Contact Form
**POST** `/api/contact/submit/`

Request body:
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "message": "I'm interested in your services..."
}
```

Response:
```json
{
    "success": true,
    "message": "Thank you for your submission. We will respond within 24 hours.",
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "company": "Acme Corp",
        "message": "I'm interested in your services...",
        "created_at": "2024-04-05T10:30:00Z"
    },
    "email_status": {
        "company_email_sent": true,
        "customer_confirmation_sent": true
    }
}
```

### List All Contact Submissions
**GET** `/api/contact/submissions/`

### Get Specific Submission
**GET** `/api/contact/submissions/<id>/`

## Admin Panel
Access the Django admin panel at `http://localhost:8000/admin/` with your superuser credentials.

## Features

- Contact form submission via REST API
- Automatic email notification to `synexinnovation@gmail.com`
- Customer confirmation email
- Contact submissions stored in database
- Admin panel to manage submissions
- CORS enabled for frontend integration
- Email templates with HTML formatting

## Email Service

The `email_service.py` module handles:
- Sending contact details to company email
- Sending confirmation email to customer
- HTML and plain text email formatting
- Error handling and logging

## Project Structure

```
backend/
├── config/              # Project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── contact/             # Contact app
│   ├── models.py        # Contact submission model
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # App URL routing
│   ├── email_service.py # Email logic
│   └── admin.py         # Admin configuration
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── .env.example         # Environment variables template
```

## Troubleshooting

### Email not sending
1. Check `.env` file has correct Gmail credentials
2. Verify app password is correct (not your Gmail password)
3. Check Gmail account has 2-Step Verification enabled
4. Verify `CONTACT_EMAIL_TO` in `.env`

### Database errors
Run migrations again:
```bash
python manage.py makemigrations
python manage.py migrate
```

### CORS errors
Update `CORS_ALLOWED_ORIGINS` in `.env` to include your frontend URL.

## Development

For development without actually sending emails, change the email backend in `.env`:
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This will print emails to the console instead.
