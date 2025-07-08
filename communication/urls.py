from django.urls import path
from . import views

urlpatterns = [
    path('email-form/', views.send_email, name='email_form'),
    path('email/sent/<str:receiver_email>/', views.email_sent, name='email_sent'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent_items/', views.outbox, name='sent_items'),
    path('reply-emails/', views.reply_emails, name='replies'),
    path('drafts/', views.drafts, name='drafts'),
    path('deleted_items/', views.deleted_items, name='deleted_items'),
    path('email-detail/<int:pk>/', views.email_detail, name='email_detail'),
    path('email_delete/<int:pk>/', views.email_delete, name='email_delete'),
    path('email-reply/<int:pk>/', views.reply_email, name='reply_email'),
    path('generate_ai/', views.generate_ai_response, name='generate_ai'),
    path('generate_email_response/', views.email_response, name='generate_email_response'),
    path('email_response/<str:subject>/<str:message>/', views.email_response, name='email_response'),
    path('templates/', views.templates_view, name='templates'),
    path('get-child-template-types/<int:parent_template_type_id>/', views.get_child_template_types, name='get_child_templates'),
    path('get-templates/<int:child_template_type_id>/', views.get_templates, name='get_templates'),
    path('email_form/<str:template_type>/', views.send_email, name='email_form'),
    path('schedule_email/', views.schedule_email, name='schedule_email'),
    path('scheduled_emails/', views.view_scheduled_emails, name='scheduled_emails'),
    path('send_scheduled_email/<pk>/', views.send_scheduled_email, name='send_scheduled_email'),
    # path('send_reminder_email/<pk>/', views.send_reminder_email, name='send_remainder_email'),
]
