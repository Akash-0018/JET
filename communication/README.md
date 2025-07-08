# Communication App

This Django app handles all email and communication functionality in the JET system, including email sending, templates, and AI-generated content.

## Features

- Email sending and management
- Email templates
- Scheduled emails and reminders
- AI-generated email content

## Models

- `Email_Message`: Represents email messages sent within the system
- `ParentTemplateType` and `ChildTemplateType`: Hierarchical organization of email templates
- `Template`: Email templates
- `ScheduledEmail`: Emails scheduled to be sent at a future time
- `ReminderEmail`: Reminder emails for scheduled events

## External Dependencies

- Ollama API for AI-generated content
- Django's email system for sending emails

## Views

- Email composition and sending
- Inbox, outbox, and drafts management
- Template selection
- AI content generation

## Usage

The Communication app integrates with the Core app for user information and provides a comprehensive email solution within the JET system.
