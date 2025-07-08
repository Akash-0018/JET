from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Email_Message(models.Model):
    From = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_emails')
    TO = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails')    
    cc_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cc_emails')
    bcc_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bcc_emails')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Email from {self.From} to {self.TO}"

    def get_replies(self):
        return Email_Message.objects.filter(replied_to=self)
    
    def save_to_inbox(self, user):
        """
        Saves a copy of the email to the inbox of the specified user.

        Args:
            user (User): The user whose inbox the email should be saved to.
        """
        # Create a new Email_Message instance for the inbox copy
        inbox_email = Email_Message(
            From=self.From,
            TO=user,
            CC=self.cc_users,
            BCC=self.bcc_users,
            subject=self.subject,
            message=self.message,
            sent=True  # Mark as sent since it's a copy
        )

        # Save the inbox copy to the database
        inbox_email.save()

        # Create a reply relationship for the inbox copy
        inbox_email.replies.add(self)
    
    @property
    def is_reply(self):
        return self.replied_to is not None

    @property
    def original_email(self):
        if self.is_reply:
            return self.replied_to
        return None

    @property
    def reply_emails(self):
        if self.is_reply:
            return Email_Message.objects.filter(replied_to=self.replied_to)
        return Email_Message.objects.filter(replied_to=self)


class ParentTemplateType(models.Model):
    name = models.CharField(max_length=255)

class ChildTemplateType(models.Model):
    parent_template_type = models.ForeignKey(ParentTemplateType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Select Template type')

class Template(models.Model):
    child_template_type = models.ForeignKey(ChildTemplateType, on_delete=models.CASCADE, null=True)  # Allow null initially
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=10000, null=True)

class ScheduledEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_emails_sent')
    receivers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scheduled_emails_received')
    cc_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scheduled_emails_cc', blank=True)
    bcc_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scheduled_emails_bcc', blank=True)
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Email from {self.sender} to {', '.join([receiver.username for receiver in self.receivers.all()])} scheduled for {self.scheduled_time}"
        
class ReminderEmail(models.Model):
    scheduled_email = models.ForeignKey(ScheduledEmail, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminder_emails_sent')
    receivers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reminder_emails_received')
