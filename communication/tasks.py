from celery import shared_task
from django.utils import timezone
from .models import ScheduledEmail
from django.core.mail import EmailMessage, get_connection

@shared_task
def send_scheduled_emails():
    now = timezone.now()
    scheduled_emails = ScheduledEmail.objects.filter(scheduled_time__lte=now, sent=False)

    for scheduled_email in scheduled_emails:
        email_message = EmailMessage(
            subject=scheduled_email.subject,
            body=scheduled_email.message,
            from_email=scheduled_email.sender.email,
            to=[receiver.email for receiver in scheduled_email.receivers.all()],
            cc=[cc_user.email for cc_user in scheduled_email.cc_users.all()],
            bcc=[bcc_user.email for bcc_user in scheduled_email.bcc_users.all()]
        )

        try:
            connection = get_connection(backend='communication.custom_email_backend.CustomEmailBackend')
            email_message.connection = connection
            email_message.send()
            scheduled_email.sent = True
            scheduled_email.save()
        except Exception as e:
            print(f"Error sending email: {e}")
