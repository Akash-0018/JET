from django.contrib import admin
from .models import Email_Message, ParentTemplateType, ChildTemplateType, Template, ScheduledEmail, ReminderEmail

@admin.register(Email_Message)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'From', 'TO', 'sent', 'deleted', 'created_at')
    search_fields = ('subject', 'From__username', 'TO__username')
    list_filter = ('sent', 'deleted', 'created_at')

@admin.register(ParentTemplateType)
class ParentTemplateTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ChildTemplateType)
class ChildTemplateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_template_type')
    search_fields = ('name', 'parent_template_type__name')

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'child_template_type')
    search_fields = ('name', 'content', 'child_template_type__name')

@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'scheduled_time', 'sent')
    search_fields = ('subject', 'sender__username')
    list_filter = ('sent', 'scheduled_time')

@admin.register(ReminderEmail)
class ReminderEmailAdmin(admin.ModelAdmin):
    list_display = ('scheduled_email', 'reminder_time', 'sent', 'sender')
    search_fields = ('scheduled_email__subject', 'sender__username')
    list_filter = ('sent', 'reminder_time')
