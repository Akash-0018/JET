from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from PIL import Image
import os

class CustomUserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
class CustomUserManager(UserManager):
    pass

class Department(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, blank=False, unique=True)
    About = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(unique=True)
    emp_id = models.CharField(max_length=10, blank=True)
    designation = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)  # Assuming 1 is the ID of a default department
    Date_of_birth = models.DateField(null=True, blank=True)
    contact_no = models.CharField(max_length=10, blank=True)
    expertise = models.CharField(max_length=250, blank=True)
    certifications = models.CharField(max_length=250, blank=True)
    Date_of_joining = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=255, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    last_login_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    About = models.CharField(max_length=120, null=True, blank=True)

    def resize_profile_picture(self):
        img = Image.open(self.picture.path)
        img.thumbnail((105, 135))
        resized_image_path = os.path.join(os.path.dirname(self.profile_picture.path), 'resized_', os.path.basename(self.profile_picture.path))
        img.save(resized_image_path)

    def __str__(self):
        if self.department:
            return f"{self.user.username} - {self.department.name}"
        else:
            return f"{self.user.username} - No department assigned"

class Intern(models.Model):
    intern_name = models.CharField(max_length=255)
    intern_role = models.CharField(max_length=255)
    internship_duration = models.DurationField(null=True, blank=True) 
    college = models.CharField(max_length=255)
    course_at_college = models.CharField(max_length=255)
    courses_offered_by_org = models.TextField(null=True, blank=True)
    sme_sessions_number = models.PositiveIntegerField(default=0)
    sme_sessions_duration = models.DurationField(null=True, blank=True)
    sme_sessions_date = models.DateField(null=True, blank=True)
    sme_session_attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sme_sessions', blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project_worked = models.TextField(null=True, blank=True)
    remarkable_contribution = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email_id = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    linkedin_id = models.URLField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Intern: {self.intern_name} - Role: {self.intern_role}"

class SMEdetails(models.Model):
    date = models.DateField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_details_handled')
    audience = models.CharField(max_length=10, default='employee')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='department_details_participants')
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Details for Department: {self.title if self.title else 'Unnamed Department'}"
