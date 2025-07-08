from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from core.models import User
from .models import Email_Message, ParentTemplateType, ChildTemplateType, Template, ScheduledEmail, ReminderEmail
from .forms import EmailForm, ReplyEmailForm, ScheduledEmailForm, ReminderEmailForm
from .api import generate_email_response_function
from .email_sender import finalize_and_send_email

@login_required
def send_email(request, template_type=None):
    import logging
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        
        # Log form data for debugging
        logger.info(f"Form data: {request.POST}")
        
        if form.is_valid():
            # Create email object without saving to allow external email addresses
            email = form.save(commit=False)
            email.From = request.user
            email.sent = True
            
            # Check if TO is a valid user or an external email address
            to_email = request.POST.get('TO', '')
            to_user = None
            
            # If TO is a select field with user ID
            if to_email and to_email.isdigit():
                try:
                    to_user = User.objects.get(id=int(to_email))
                    email.TO = to_user
                    logger.info(f"Using internal user as recipient: {to_user.email}")
                except User.DoesNotExist:
                    logger.warning(f"User with ID {to_email} not found")
                    messages.error(request, f"User with ID {to_email} not found")
                    return render(request, 'email_form.html', {'form': form})
            
            # Now save the email
            email.save()

            # Handle CC recipients - try to match with users and store in M2M field
            cc_emails = request.POST.get('cc', '').split(',')
            for cc_email in cc_emails:
                cc_email = cc_email.strip()
                if cc_email:
                    try:
                        # Try to find an existing user
                        cc_user = User.objects.get(email=cc_email)
                        email.cc_users.add(cc_user)
                        logger.info(f"Added CC internal user: {cc_user.email}")
                    except User.DoesNotExist:
                        # We'll handle external email addresses in finalize_and_send_email
                        logger.info(f"CC email not found as user: {cc_email}, will use directly")

            # Handle BCC recipients - try to match with users and store in M2M field
            bcc_emails = request.POST.get('bcc', '').split(',')
            for bcc_email in bcc_emails:
                bcc_email = bcc_email.strip()
                if bcc_email:
                    try:
                        # Try to find an existing user
                        bcc_user = User.objects.get(email=bcc_email)
                        email.bcc_users.add(bcc_user)
                        logger.info(f"Added BCC internal user: {bcc_user.email}")
                    except User.DoesNotExist:
                        # We'll handle external email addresses in finalize_and_send_email
                        logger.info(f"BCC email not found as user: {bcc_email}, will use directly")

            # Try to send the email via the email_sender
            logger.info("Calling finalize_and_send_email")
            return finalize_and_send_email(request, email, form)
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            return render(request, 'email_form.html', {'form': form})
    else:
        # Handle GET request
        message = request.GET.get('message', '')
        
        initial_data = {
            'message': message
        }
        
        if template_type:
            try:
                template = Template.objects.get(name=template_type)
                initial_data.update({
                    'subject': template.name,
                    'message': template.content
                })
            except Template.DoesNotExist:
                pass
                
        form = EmailForm(initial=initial_data)
        return render(request, 'email_form.html', {'form': form})

        form = EmailForm(initial=initial_data)
        return render(request, 'email_form.html', {'form': form})

@login_required
def email_sent(request, receiver_email):
    context = {'receiver_email': receiver_email}
    return render(request, 'email_sent.html', context)

@login_required
def inbox(request):
    emails = Email_Message.objects.filter(TO=request.user, deleted=False).order_by('-created_at')
    context = {'emails': emails}
    return render(request, 'inbox.html', context)

@login_required
def outbox(request):
    emails = Email_Message.objects.filter(From=request.user, deleted=False, sent=True).order_by('-created_at')
    context = {'emails': emails}
    return render(request, 'sent_items.html', context)

@login_required
def drafts(request):
    emails = Email_Message.objects.filter(From=request.user, sent=False, deleted=False).order_by('-created_at')
    context = {'emails': emails}
    return render(request, 'drafts.html', context)

@login_required
def deleted_items(request):
    emails = Email_Message.objects.filter(Q(From=request.user) | Q(TO=request.user), deleted=True).order_by('-created_at')
    context = {'emails': emails}
    return render(request, 'deleted_items.html', context)

@login_required
def reply_emails(request):
    emails = Email_Message.objects.filter(replied_to__isnull=False, From=request.user).order_by('-created_at')
    context = {'emails': emails}
    return render(request, 'replies.html', context)

@login_required
def email_detail(request, pk):
    email = get_object_or_404(Email_Message, pk=pk)
    context = {'email': email}
    return render(request, 'email_detail.html', context)

@login_required
def email_delete(request, pk):
    email = get_object_or_404(Email_Message, pk=pk)
    if request.method == 'POST':
        email.deleted = True
        email.save()
        return redirect('inbox')
    return render(request, 'email_delete.html', {'email': email})

@login_required
def reply_email(request, pk):
    original_email = get_object_or_404(Email_Message, pk=pk)
    
    if request.method == 'POST':
        form = ReplyEmailForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.From = request.user
            reply.TO = original_email.From  # Reply to the sender of the original email
            reply.sent = True
            reply.replied_to = original_email
            reply.save()
            
            # Handle CC recipients
            cc_emails = request.POST.get('cc', '').split(',')
            for cc_email in cc_emails:
                cc_email = cc_email.strip()
                if cc_email:
                    try:
                        cc_user = User.objects.get(email=cc_email)
                        reply.cc_users.add(cc_user)
                    except User.DoesNotExist:
                        pass

            # Handle BCC recipients
            bcc_emails = request.POST.get('bcc', '').split(',')
            for bcc_email in bcc_emails:
                bcc_email = bcc_email.strip()
                if bcc_email:
                    try:
                        bcc_user = User.objects.get(email=bcc_email)
                        reply.bcc_users.add(bcc_user)
                    except User.DoesNotExist:
                        pass
                        
            # Try to send the email
            return finalize_and_send_email(request, reply, form)
        else:
            return render(request, 'reply_email.html', {'form': form, 'original_email': original_email})
    else:
        # Default subject with "Re: " prefix if not already there
        subject = original_email.subject
        if not subject.startswith('Re:'):
            subject = f'Re: {subject}'
            
        # Prepare the form with initial values
        initial_data = {
            'subject': subject,
            'message': f"\n\n---------- Original Message ----------\nFrom: {original_email.From}\nDate: {original_email.created_at.strftime('%a, %d %b %Y %H:%M:%S')}\nSubject: {original_email.subject}\n\n{original_email.message}"
        }
        
        form = ReplyEmailForm(initial=initial_data)
        return render(request, 'reply_email.html', {'form': form, 'original_email': original_email})

@login_required
def generate_ai_response(request):
    from .forms import EmailForm
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        prompt = request.POST.get('prompt', '')
        
        if prompt:
            # Generate AI response using the prompt
            api_prompt = f"Generate a professional email with the following instructions: {prompt}"
            generated_text = generate_email_response_function(api_prompt)
            
            # Get subject from form or default
            subject = request.POST.get('subject', 'Generated Email Subject')
            
            return render(request, 'generate_ai.html', {
                'form': form, 
                'generated_text': generated_text,
                'subject': subject,
                'prompt': prompt
            })
    else:
        form = EmailForm()
        
    return render(request, 'generate_ai.html', {'form': form})

@login_required
def email_response(request, subject=None, message=None):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        regenerate = request.POST.get('regenerate') == 'true'
        
        prompt = f"Generate a professional email for subject: {subject}, with the following details: {message}"
        response = generate_email_response_function(prompt, regenerate)
        
        return JsonResponse({'response': response})
    else:
        return render(request, 'generate_ai.html', {'subject': subject, 'message': message})

@login_required
def templates_view(request):
    parent_template_types = ParentTemplateType.objects.all()
    child_template_types = ChildTemplateType.objects.all()
    templates = Template.objects.all()

    context = {
        'parent_template_types': parent_template_types,
        'child_template_types': child_template_types,
        'templates': templates
    }

    return render(request, 'templates.html', context)

@login_required
def get_child_template_types(request, parent_template_type_id):
    child_template_types = ChildTemplateType.objects.filter(parent_template_type_id=parent_template_type_id)
    data = [{'id': ct.id, 'name': ct.name} for ct in child_template_types]
    return JsonResponse(data, safe=False)

@login_required
def get_templates(request, child_template_type_id):
    templates = Template.objects.filter(child_template_type_id=child_template_type_id)
    data = [{'id': t.id, 'name': t.name, 'content': t.content} for t in templates]
    return JsonResponse(data, safe=False)

@login_required
def schedule_email(request):
    if request.method == 'POST':
        form = ScheduledEmailForm(request.POST)
        if form.is_valid():
            scheduled_email = form.save(commit=False)
            scheduled_email.sender = request.user
            scheduled_email.save()
            
            # Process receivers
            receivers_emails = request.POST.get('receivers_emails', '').split(',')
            for receiver_email in receivers_emails:
                receiver_email = receiver_email.strip()
                if receiver_email:
                    try:
                        receiver = User.objects.get(email=receiver_email)
                        scheduled_email.receivers.add(receiver)
                    except User.DoesNotExist:
                        pass
            
            # Process CC
            cc_emails = request.POST.get('cc', '').split(',')
            for cc_email in cc_emails:
                cc_email = cc_email.strip()
                if cc_email:
                    try:
                        cc_user = User.objects.get(email=cc_email)
                        scheduled_email.cc_users.add(cc_user)
                    except User.DoesNotExist:
                        pass
            
            # Process BCC
            bcc_emails = request.POST.get('bcc', '').split(',')
            for bcc_email in bcc_emails:
                bcc_email = bcc_email.strip()
                if bcc_email:
                    try:
                        bcc_user = User.objects.get(email=bcc_email)
                        scheduled_email.bcc_users.add(bcc_user)
                    except User.DoesNotExist:
                        pass
            
            # Check if reminder is requested
            if 'set_reminder' in request.POST:
                reminder_form = ReminderEmailForm(request.POST)
                if reminder_form.is_valid():
                    reminder = reminder_form.save(commit=False)
                    reminder.scheduled_email = scheduled_email
                    reminder.sender = request.user
                    reminder.save()
                    
                    # Add the same receivers to the reminder
                    for receiver in scheduled_email.receivers.all():
                        reminder.receivers.add(receiver)
            
            messages.success(request, 'Email scheduled successfully!')
            return redirect('scheduled_emails')
        else:
            messages.error(request, 'There was an error with your form. Please check the data and try again.')
    else:
        form = ScheduledEmailForm()
        reminder_form = ReminderEmailForm()
    
    return render(request, 'schedule_email.html', {
        'form': form,
        'reminder_form': reminder_form
    })

@login_required
def view_scheduled_emails(request):
    scheduled_emails = ScheduledEmail.objects.filter(sender=request.user).order_by('scheduled_time')
    return render(request, 'scheduled_emails.html', {'emails': scheduled_emails})

@login_required
def send_scheduled_email(request, pk):
    email = get_object_or_404(ScheduledEmail, pk=pk)
    
    if email.sender != request.user:
        messages.error(request, "You don't have permission to send this email.")
        return redirect('scheduled_emails')
    
    # Create an EmailMessage instance
    email_message = Email_Message(
        From=email.sender,
        TO=email.receivers.first(),  # Assuming there's at least one receiver
        subject=email.subject,
        message=email.message,
        sent=True
    )
    email_message.save()
    
    # Add CC and BCC users
    for cc_user in email.cc_users.all():
        email_message.cc_users.add(cc_user)
    
    for bcc_user in email.bcc_users.all():
        email_message.bcc_users.add(bcc_user)
    
    # Add other receivers as BCC
    for receiver in email.receivers.all()[1:]:  # Skip the first one, which is the main recipient
        email_message.bcc_users.add(receiver)
    
    # Send the email
    try:
        finalize_and_send_email(request, email_message, None)
        
        # Mark the scheduled email as sent
        email.sent = True
        email.save()
        
        messages.success(request, 'Email sent successfully!')
    except Exception as e:
        messages.error(request, f'Error sending email: {str(e)}')
    
    return redirect('scheduled_emails')

@login_required
def test_email(request):
    """
    View for testing email functionality.
    Shows SMTP configuration and allows sending a test email.
    """
    import logging
    from django.core.mail import send_mail
    from django.conf import settings
    from smtplib import SMTP
    
    logger = logging.getLogger(__name__)
    
    # Configuration information
    email_config = {
        'backend': settings.EMAIL_BACKEND,
        'host': settings.EMAIL_HOST,
        'port': settings.EMAIL_PORT,
        'use_tls': settings.EMAIL_USE_TLS,
        'use_ssl': settings.EMAIL_USE_SSL,
        'username': settings.EMAIL_HOST_USER,
        'password': '*****' if settings.EMAIL_HOST_PASSWORD else 'Not configured'
    }
    
    connection_test = {
        'success': False,
        'message': 'Not tested yet'
    }
    
    send_test = {
        'success': False,
        'message': 'Not tested yet'
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'test_connection':
            try:
                # Test SMTP connection
                server = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                server.set_debuglevel(1)
                server.ehlo()
                
                if settings.EMAIL_USE_TLS:
                    server.starttls()
                    server.ehlo()
                    
                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                
                server.quit()
                connection_test['success'] = True
                connection_test['message'] = 'Connection successful!'
                
            except Exception as e:
                connection_test['success'] = False
                connection_test['message'] = f'Connection failed: {str(e)}'
                logger.error(f"SMTP connection test failed: {str(e)}")
        
        elif action == 'send_test':
            to_email = request.POST.get('to_email')
            if not to_email:
                send_test['message'] = 'Please provide a recipient email address.'
            else:
                try:
                    # Send a test email
                    send_result = send_mail(
                        subject='JET Email Test',
                        message='This is a test email from JET application.',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[to_email],
                        fail_silently=False
                    )
                    
                    if send_result:
                        send_test['success'] = True
                        send_test['message'] = f'Test email sent to {to_email}!'
                    else:
                        send_test['message'] = 'Email not sent. Check server logs for details.'
                
                except Exception as e:
                    send_test['success'] = False
                    send_test['message'] = f'Failed to send: {str(e)}'
                    logger.error(f"Test email failed: {str(e)}")
    
    context = {
        'email_config': email_config,
        'connection_test': connection_test,
        'send_test': send_test
    }
    
    return render(request, 'email_test.html', context)
