from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import logging
import smtplib
from email.mime.text import MIMEText
import sys

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"CustomEmailBackend initialized with host: {settings.EMAIL_HOST}, port: {settings.EMAIL_PORT}")

    def send_messages(self, email_messages, request=None):
        """
        Override send_messages to ensure all emails are sent from a single account.
        This implementation adds extensive debugging and error handling.
        """
        if not email_messages:
            logger.warning("No email messages to send")
            return 0
        
        sent_count = 0
        
        for message in email_messages:
            original_from = message.from_email
            message.from_email = settings.EMAIL_HOST_USER  # Ensure the sender is the specified email
            
            # Log message details
            logger.info(f"Preparing to send email:")
            logger.info(f"  From: {message.from_email} (original: {original_from})")
            logger.info(f"  To: {message.to}")
            logger.info(f"  CC: {message.cc}")
            logger.info(f"  BCC: {message.bcc}")
            logger.info(f"  Subject: {message.subject}")
            
            # Verify recipients
            if not message.to:
                logger.error("Cannot send email: No recipients specified")
                continue
            
            # Try to connect directly to SMTP server for debugging
            if settings.EMAIL_DEBUG:
                try:
                    logger.debug("Testing direct SMTP connection...")
                    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    smtp.set_debuglevel(1)  # Enable debug output
                    smtp.ehlo()  # Say hello to the server
                    
                    if settings.EMAIL_USE_TLS:
                        smtp.starttls()
                        smtp.ehlo()  # Say hello again after TLS
                    
                    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    logger.debug("SMTP login successful")
                    
                    # Create a simple test message
                    msg = MIMEText("This is a test message from the CustomEmailBackend")
                    msg['Subject'] = "SMTP Test"
                    msg['From'] = settings.EMAIL_HOST_USER
                    msg['To'] = message.to[0]
                    
                    # Send the test message
                    smtp.sendmail(settings.EMAIL_HOST_USER, [message.to[0]], msg.as_string())
                    logger.debug("Test message sent successfully")
                    
                    smtp.quit()
                except Exception as e:
                    logger.error(f"SMTP test failed: {str(e)}")
            
        try:
            # Use the standard Django email backend to send the actual message
            sent_count = super().send_messages(email_messages)
            logger.info(f"Successfully sent {sent_count} emails")
            return sent_count
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication Error: {str(e)}")
            logger.error("Please verify your email credentials")
            return 0
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Recipients refused: {str(e)}")
            logger.error("One or more recipients were refused by the SMTP server")
            return 0
        except smtplib.SMTPException as e:
            logger.error(f"SMTP Error: {str(e)}")
            return 0
        except Exception as e:
            # Add logging for better debugging
            logger.error(f"Error sending email: {str(e)}")
            return 0
