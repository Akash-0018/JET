from django import forms
from .models import Email_Message, ScheduledEmail, ReminderEmail, Template
from django.forms import DateTimeInput

class EmailForm(forms.ModelForm):
    cc = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter CC email addresses (separated by commas)'
    }))
    bcc = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter BCC email addresses (separated by commas)'
    }))
    external_email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Or enter an external email address'
    }))

    class Meta:
        model = Email_Message
        fields = ['TO', 'subject', 'message']
        widgets = {
            'TO': forms.Select(attrs={
                'class': 'form-control custom-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional details for the AI to include in the email',
                'rows': 5
            })
        }
        
    def clean(self):
        cleaned_data = super().clean()
        to_user = cleaned_data.get('TO')
        external_email = cleaned_data.get('external_email')
        
        # Validate that at least one of TO or external_email is provided
        if not to_user and not external_email:
            raise forms.ValidationError("Please provide either a recipient user or an external email address.")
            
        return cleaned_data

class ReplyEmailForm(forms.ModelForm):
    cc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bcc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Email_Message
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'})
        }

class ScheduledEmailForm(forms.ModelForm):
    cc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bcc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    receivers_emails = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ScheduledEmail
        fields = ['subject', 'message', 'scheduled_time']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'scheduled_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }

class ReminderEmailForm(forms.ModelForm):
    class Meta:
        model = ReminderEmail
        fields = ['reminder_time']
        widgets = {
            'reminder_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }
