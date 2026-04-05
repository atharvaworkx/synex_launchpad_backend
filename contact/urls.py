"""
URL routes for contact app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_contact_form, name='submit_contact_form'),
    path('submissions/', views.contact_submissions_list, name='contact_submissions_list'),
    path('submissions/<int:pk>/', views.contact_submission_detail, name='contact_submission_detail'),
]
