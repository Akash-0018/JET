from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from django.contrib import messages
from django.conf import settings
import logging
import re
import sys
from smtplib import SMTPException

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def is_valid_email(email):
    """Validate if a string is a proper email address."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))

def finalize_and_send_email(request, email, form):
    """
    Finalizes and sends the email after customization.
    Improved to handle arbitrary email addresses and better error handling.
    """
    # Prepare recipient lists
    to_emails = []
    cc_emails = []
    bcc_emails = []
    
    # Main recipient
    if hasattr(email.TO, 'email') and email.TO.email:
        if is_valid_email(email.TO.email):
            to_emails.append(email.TO.email)
            logger.info(f"Added primary recipient: {email.TO.email}")
        else:
            logger.warning(f"Invalid primary recipient email: {email.TO.email}")
    elif hasattr(email, 'TO') and isinstance(email.TO, str) and is_valid_email(email.TO):
        to_emails.append(email.TO)
        logger.info(f"Added primary recipient from string: {email.TO}")
    
    # CC recipients
    if hasattr(email, 'cc_users') and email.cc_users:
        for user in email.cc_users.all():
            if hasattr(user, 'email') and is_valid_email(user.email):
                cc_emails.append(user.email)
                logger.info(f"Added CC recipient: {user.email}")
    
    # BCC recipients
    if hasattr(email, 'bcc_users') and email.bcc_users:
        for user in email.bcc_users.all():
            if hasattr(user, 'email') and is_valid_email(user.email):
                bcc_emails.append(user.email)
                logger.info(f"Added BCC recipient: {user.email}")
    
    # Additional recipients from form data if available
    if request and request.POST:
        # Manual CC handling
        manual_cc = request.POST.get('cc', '').split(',')
        for cc in manual_cc:
            cc = cc.strip()
            if cc and is_valid_email(cc):
                cc_emails.append(cc)
                logger.info(f"Added manual CC recipient: {cc}")
        
        # Manual BCC handling
        manual_bcc = request.POST.get('bcc', '').split(',')
        for bcc in manual_bcc:
            bcc = bcc.strip()
            if bcc and is_valid_email(bcc):
                bcc_emails.append(bcc)
                logger.info(f"Added manual BCC recipient: {bcc}")
    
    # Validate we have at least one recipient
    if not to_emails:
        error_message = 'No valid recipient email address provided.'
        logger.error(error_message)
        messages.error(request, error_message)
        return render(request, 'email_form.html', {'form': form, 'error': error_message})
    
    # Log email details
    logger.info(f"Preparing to send email:")
    logger.info(f"From: {settings.EMAIL_HOST_USER}")
    logger.info(f"To: {to_emails}")
    logger.info(f"CC: {cc_emails}")
    logger.info(f"BCC: {bcc_emails}")
    logger.info(f"Subject: {email.subject}")
    
    # Create the email message
    email_message = EmailMessage(
        subject=email.subject,
        body=email.message,
        from_email=settings.EMAIL_HOST_USER,
        to=to_emails,
        cc=cc_emails,
        bcc=bcc_emails,
        connection=get_connection()  # Get a fresh connection
    )

    # Send the email with more detailed error handling
    try:
        # Force debug output
        sent = email_message.send(fail_silently=False)
        logger.info(f"Email sent successfully (result: {sent})")
        messages.success(request, f'Email sent successfully to {", ".join(to_emails)}!')
        return redirect('sent_items')
    except SMTPException as e:
        error_message = f'SMTP Error: {str(e)}'
        logger.error(error_message)
        messages.error(request, error_message)
        return render(request, 'email_form.html', {'form': form, 'error': error_message})
    except ConnectionRefusedError:
        error_message = 'Connection refused by mail server. Please check your network and server settings.'
        logger.error(error_message)
        messages.error(request, error_message)
        return render(request, 'email_form.html', {'form': form, 'error': error_message})
    except Exception as e:
        error_message = f'Error sending email: {str(e)}'
        logger.error(error_message)
        messages.error(request, error_message)
        return render(request, 'email_form.html', {'form': form, 'error': error_message})
