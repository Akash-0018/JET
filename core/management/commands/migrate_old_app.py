from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.apps import apps

class Command(BaseCommand):
    help = 'Migrate data from the old app structure to new apps'

    def handle(self, *args, **options):
        # Check if app tables exist
        old_app_exists = False
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='app_user'"
            )
            old_app_exists = cursor.fetchone() is not None
        
        if not old_app_exists:
            self.stdout.write(self.style.WARNING('Old app tables do not exist. Migration skipped.'))
            return
        
        # Migrate user data
        self.migrate_users()
        
        # Migrate department data
        self.migrate_departments()
        
        # Migrate profile data
        self.migrate_profiles()
        
        # Migrate intern data
        self.migrate_interns()
        
        # Migrate SMEdetails data
        self.migrate_smedetails()
        
        # Migrate course data
        self.migrate_courses()
        
        # Migrate certification data
        self.migrate_certifications()
        
        # Migrate user enrollment data
        self.migrate_user_enrollments()
        
        # Migrate user certification data
        self.migrate_user_certifications()
        
        # Migrate metrics report data
        self.migrate_metrics_reports()
        
        # Migrate email data
        self.migrate_emails()
        
        # Migrate template data
        self.migrate_templates()
        
        # Migrate scheduled email data
        self.migrate_scheduled_emails()
        
        self.stdout.write(self.style.SUCCESS('Successfully migrated data from old app to new apps'))
    
    @transaction.atomic
    def migrate_users(self):
        from core.models import User as NewUser
        from app.models import User as OldUser
        
        old_users = OldUser.objects.all()
        for old_user in old_users:
            # Check if user already exists
            if not NewUser.objects.filter(username=old_user.username).exists():
                new_user = NewUser(
                    username=old_user.username,
                    About=old_user.About,
                    profile_picture=old_user.profile_picture,
                    first_name=old_user.first_name,
                    last_name=old_user.last_name,
                    email=old_user.email,
                    emp_id=old_user.emp_id,
                    designation_id=old_user.designation_id,
                    Date_of_birth=old_user.Date_of_birth,
                    contact_no=old_user.contact_no,
                    expertise=old_user.expertise,
                    certifications=old_user.certifications,
                    Date_of_joining=old_user.Date_of_joining,
                    department=old_user.department,
                    password=old_user.password,
                    is_superuser=old_user.is_superuser,
                    is_staff=old_user.is_staff,
                    is_active=old_user.is_active,
                    date_joined=old_user.date_joined,
                    last_login=old_user.last_login
                )
                new_user.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_users.count()} users'))
    
    @transaction.atomic
    def migrate_departments(self):
        from core.models import Department as NewDepartment
        from app.models import Department as OldDepartment
        
        old_departments = OldDepartment.objects.all()
        for old_dept in old_departments:
            # Check if department already exists
            if not NewDepartment.objects.filter(name=old_dept.name).exists():
                new_dept = NewDepartment(
                    id=old_dept.id,  # Preserve ID for relationships
                    name=old_dept.name,
                    parent_id=old_dept.parent_id
                )
                new_dept.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_departments.count()} departments'))
    
    @transaction.atomic
    def migrate_profiles(self):
        from core.models import Profile as NewProfile
        from app.models import Profile as OldProfile
        
        old_profiles = OldProfile.objects.all()
        for old_profile in old_profiles:
            # Check if profile already exists
            if not NewProfile.objects.filter(user_id=old_profile.user_id).exists():
                new_profile = NewProfile(
                    user_id=old_profile.user_id,
                    profile_picture=old_profile.profile_picture,
                    last_login_time=old_profile.last_login_time,
                    score=old_profile.score,
                    department_id=old_profile.department_id,
                    About=old_profile.About
                )
                new_profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_profiles.count()} profiles'))

    @transaction.atomic
    def migrate_interns(self):
        from core.models import Intern as NewIntern
        from app.models import Intern as OldIntern
        
        old_interns = OldIntern.objects.all()
        for old_intern in old_interns:
            # Check if intern already exists
            if not NewIntern.objects.filter(user_id=old_intern.user_id).exists():
                new_intern = NewIntern(
                    intern_name=old_intern.intern_name,
                    intern_role=old_intern.intern_role,
                    internship_duration=old_intern.internship_duration,
                    college=old_intern.college,
                    course_at_college=old_intern.course_at_college,
                    courses_offered_by_org=old_intern.courses_offered_by_org,
                    sme_sessions_number=old_intern.sme_sessions_number,
                    sme_sessions_duration=old_intern.sme_sessions_duration,
                    sme_sessions_date=old_intern.sme_sessions_date,
                    start_date=old_intern.start_date,
                    end_date=old_intern.end_date,
                    project_worked=old_intern.project_worked,
                    remarkable_contribution=old_intern.remarkable_contribution,
                    contact_number=old_intern.contact_number,
                    email_id=old_intern.email_id,
                    address=old_intern.address,
                    linkedin_id=old_intern.linkedin_id,
                    user_id=old_intern.user_id
                )
                new_intern.save()
                
                # Migrate ManyToMany relationships
                for attendee in old_intern.sme_session_attendees.all():
                    new_intern.sme_session_attendees.add(attendee)
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_interns.count()} interns'))
    
    @transaction.atomic
    def migrate_smedetails(self):
        from core.models import SMEdetails as NewSMEdetails
        from app.models import SMEdetails as OldSMEdetails
        
        old_smedetails = OldSMEdetails.objects.all()
        for old_sme in old_smedetails:
            # Check if SME detail already exists
            existing = NewSMEdetails.objects.filter(
                date=old_sme.date,
                title=old_sme.title,
                handled_by_id=old_sme.handled_by_id
            ).exists()
            
            if not existing:
                new_sme = NewSMEdetails(
                    date=old_sme.date,
                    duration=old_sme.duration,
                    handled_by_id=old_sme.handled_by_id,
                    audience=old_sme.audience,
                    title=old_sme.title
                )
                new_sme.save()
                
                # Migrate ManyToMany relationships
                for participant in old_sme.participants.all():
                    new_sme.participants.add(participant)
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_smedetails.count()} SME details'))

    @transaction.atomic
    def migrate_courses(self):
        from learning.models import Course as NewCourse
        from app.models import Course as OldCourse
        
        old_courses = OldCourse.objects.all()
        for old_course in old_courses:
            # Check if course already exists
            if not NewCourse.objects.filter(name=old_course.name, user_id=old_course.user_id).exists():
                new_course = NewCourse(
                    name=old_course.name,
                    description=old_course.description,
                    created_at=old_course.created_at,
                    updated_at=old_course.updated_at,
                    user_id=old_course.user_id,
                    link=old_course.link,
                    progress=old_course.progress,
                    points=old_course.points
                )
                new_course.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_courses.count()} courses'))

    @transaction.atomic
    def migrate_certifications(self):
        from learning.models import Certification as NewCertification
        from app.models import Certification as OldCertification
        
        old_certifications = OldCertification.objects.all()
        for old_cert in old_certifications:
            # Check if certification already exists
            if not NewCertification.objects.filter(name=old_cert.name, user_id=old_cert.user_id).exists():
                new_cert = NewCertification(
                    name=old_cert.name,
                    description=old_cert.description,
                    created_at=old_cert.created_at,
                    updated_at=old_cert.updated_at,
                    user_id=old_cert.user_id,
                    link=old_cert.link,
                    progress=old_cert.progress,
                    points=old_cert.points
                )
                new_cert.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_certifications.count()} certifications'))

    @transaction.atomic
    def migrate_user_enrollments(self):
        from learning.models import UserEnrollment as NewUserEnrollment
        from app.models import UserEnrollment as OldUserEnrollment
        
        old_enrollments = OldUserEnrollment.objects.all()
        for old_enroll in old_enrollments:
            # Check if enrollment already exists
            existing = NewUserEnrollment.objects.filter(
                user_id=old_enroll.user_id,
                course_id=old_enroll.course_id,
                certification_id=old_enroll.certification_id
            ).exists()
            
            if not existing:
                new_enroll = NewUserEnrollment(
                    user_id=old_enroll.user_id,
                    course_id=old_enroll.course_id,
                    course_enrolled_at=old_enroll.course_enrolled_at,
                    course_completed_at=old_enroll.course_completed_at,
                    course_progress=old_enroll.course_progress,
                    certification_id=old_enroll.certification_id,
                    certification_enrolled_at=old_enroll.certification_enrolled_at,
                    certification_completed_at=old_enroll.certification_completed_at,
                    certification_progress=old_enroll.certification_progress
                )
                new_enroll.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_enrollments.count()} user enrollments'))

    @transaction.atomic
    def migrate_user_certifications(self):
        from learning.models import UserCertification as NewUserCertification
        from app.models import UserCertification as OldUserCertification
        
        old_user_certs = OldUserCertification.objects.all()
        for old_user_cert in old_user_certs:
            # Check if user certification already exists
            existing = NewUserCertification.objects.filter(
                user_id=old_user_cert.user_id,
                certification_id=old_user_cert.certification_id
            ).exists()
            
            if not existing:
                new_user_cert = NewUserCertification(
                    user_id=old_user_cert.user_id,
                    certification_id=old_user_cert.certification_id,
                    completed_at=old_user_cert.completed_at,
                    enrolled_at=old_user_cert.enrolled_at
                )
                new_user_cert.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_user_certs.count()} user certifications'))

    @transaction.atomic
    def migrate_metrics_reports(self):
        from learning.models import MetricsReport as NewMetricsReport
        from app.models import MetricsReport as OldMetricsReport
        
        old_metrics = OldMetricsReport.objects.all()
        for old_metric in old_metrics:
            # Check if metrics report already exists
            if not NewMetricsReport.objects.filter(year=old_metric.year).exists():
                new_metric = NewMetricsReport(
                    year=old_metric.year,
                    courses_completed=old_metric.courses_completed,
                    certifications=old_metric.certifications,
                    employees_trained=old_metric.employees_trained,
                    interns=old_metric.interns,
                    intern_projects=old_metric.intern_projects,
                    sme_sessions=old_metric.sme_sessions
                )
                new_metric.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_metrics.count()} metrics reports'))

    @transaction.atomic
    def migrate_emails(self):
        from communication.models import Email_Message as NewEmail
        from app.models import Email_Message as OldEmail
        
        # First pass to create all email objects
        old_emails = OldEmail.objects.all()
        email_mapping = {}  # Maps old email IDs to new email objects
        
        for old_email in old_emails:
            # Check if email already exists
            existing = NewEmail.objects.filter(
                From_id=old_email.From_id,
                TO_id=old_email.TO_id,
                subject=old_email.subject,
                created_at=old_email.created_at
            ).exists()
            
            if not existing:
                new_email = NewEmail(
                    From_id=old_email.From_id,
                    TO_id=old_email.TO_id,
                    subject=old_email.subject,
                    message=old_email.message,
                    sent=old_email.sent,
                    deleted=old_email.deleted,
                    created_at=old_email.created_at,
                    updated_at=old_email.updated_at,
                    # Don't set replied_to yet, we'll do that in a second pass
                )
                new_email.save()
                email_mapping[old_email.id] = new_email
                
                # Migrate ManyToMany relationships
                for cc_user in old_email.cc_users.all():
                    new_email.cc_users.add(cc_user)
                
                for bcc_user in old_email.bcc_users.all():
                    new_email.bcc_users.add(bcc_user)
        
        # Second pass to set up reply relationships
        for old_email in old_emails:
            if old_email.replied_to_id and old_email.replied_to_id in email_mapping:
                new_email = email_mapping[old_email.id]
                new_email.replied_to = email_mapping[old_email.replied_to_id]
                new_email.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_emails.count()} emails'))

    @transaction.atomic
    def migrate_templates(self):
        from communication.models import ParentTemplateType as NewParentType
        from communication.models import ChildTemplateType as NewChildType
        from communication.models import Template as NewTemplate
        from app.models import ParentTemplateType as OldParentType
        from app.models import ChildTemplateType as OldChildType
        from app.models import Template as OldTemplate
        
        # Migrate parent template types
        old_parent_types = OldParentType.objects.all()
        for old_parent in old_parent_types:
            if not NewParentType.objects.filter(name=old_parent.name).exists():
                new_parent = NewParentType(
                    id=old_parent.id,  # Keep the same ID for relationships
                    name=old_parent.name
                )
                new_parent.save()
        
        # Migrate child template types
        old_child_types = OldChildType.objects.all()
        for old_child in old_child_types:
            if not NewChildType.objects.filter(name=old_child.name, parent_template_type_id=old_child.parent_template_type_id).exists():
                new_child = NewChildType(
                    id=old_child.id,  # Keep the same ID for relationships
                    parent_template_type_id=old_child.parent_template_type_id,
                    name=old_child.name
                )
                new_child.save()
        
        # Migrate templates
        old_templates = OldTemplate.objects.all()
        for old_template in old_templates:
            if not NewTemplate.objects.filter(name=old_template.name, child_template_type_id=old_template.child_template_type_id).exists():
                new_template = NewTemplate(
                    child_template_type_id=old_template.child_template_type_id,
                    name=old_template.name,
                    content=old_template.content
                )
                new_template.save()
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_parent_types.count()} parent template types, '
                                           f'{old_child_types.count()} child template types, '
                                           f'{old_templates.count()} templates'))

    @transaction.atomic
    def migrate_scheduled_emails(self):
        from communication.models import ScheduledEmail as NewScheduledEmail
        from communication.models import ReminderEmail as NewReminderEmail
        from app.models import ScheduledEmail as OldScheduledEmail
        from app.models import ReminderEmail as OldReminderEmail
        
        # Migrate scheduled emails
        old_scheduled = OldScheduledEmail.objects.all()
        scheduled_mapping = {}  # Maps old scheduled email IDs to new scheduled email objects
        
        for old_email in old_scheduled:
            # Check if scheduled email already exists
            existing = NewScheduledEmail.objects.filter(
                sender_id=old_email.sender_id,
                subject=old_email.subject,
                scheduled_time=old_email.scheduled_time
            ).exists()
            
            if not existing:
                new_email = NewScheduledEmail(
                    user_id=old_email.user_id,
                    subject=old_email.subject,
                    message=old_email.message,
                    sender_id=old_email.sender_id,
                    scheduled_time=old_email.scheduled_time,
                    sent=old_email.sent
                )
                new_email.save()
                scheduled_mapping[old_email.id] = new_email
                
                # Migrate ManyToMany relationships
                for receiver in old_email.receivers.all():
                    new_email.receivers.add(receiver)
                
                for cc_user in old_email.cc_users.all():
                    new_email.cc_users.add(cc_user)
                
                for bcc_user in old_email.bcc_users.all():
                    new_email.bcc_users.add(bcc_user)
        
        # Migrate reminder emails
        old_reminders = OldReminderEmail.objects.all()
        for old_reminder in old_reminders:
            if old_reminder.scheduled_email_id in scheduled_mapping:
                # Check if reminder email already exists
                existing = NewReminderEmail.objects.filter(
                    scheduled_email=scheduled_mapping[old_reminder.scheduled_email_id],
                    reminder_time=old_reminder.reminder_time
                ).exists()
                
                if not existing:
                    new_reminder = NewReminderEmail(
                        scheduled_email=scheduled_mapping[old_reminder.scheduled_email_id],
                        reminder_time=old_reminder.reminder_time,
                        sent=old_reminder.sent,
                        sender_id=old_reminder.sender_id
                    )
                    new_reminder.save()
                    
                    # Migrate ManyToMany relationships
                    for receiver in old_reminder.receivers.all():
                        new_reminder.receivers.add(receiver)
        
        self.stdout.write(self.style.SUCCESS(f'Migrated {old_scheduled.count()} scheduled emails and {old_reminders.count()} reminder emails'))
