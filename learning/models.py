from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Course(models.Model):
    POINTS_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.URLField(unique=True, blank=False)
    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),  # Minimum value is 0
            MaxValueValidator(100)    # Maximum value is 100
        ]
    )
    points = models.CharField(max_length=1, choices=POINTS_CHOICES, default='0')

    def __str__(self):
        return self.name

class Certification(models.Model):
    POINTS_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.URLField(max_length=255)
    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),  
            MaxValueValidator(100)    
        ]
    )
    points = models.CharField(max_length=1, choices=POINTS_CHOICES, default='0')

    def __str__(self):
        return self.name

class UserEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    course_enrolled_at = models.DateTimeField(null=True, blank=True)
    course_completed_at = models.DateTimeField(null=True, blank=True)
    course_progress = models.IntegerField(default=0)

    certification = models.ForeignKey('Certification', on_delete=models.CASCADE, null=True, blank=True)
    certification_enrolled_at = models.DateTimeField(null=True, blank=True)
    certification_completed_at = models.DateTimeField(null=True, blank=True)
    certification_progress = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name if self.course else self.certification.name}"
    
class UserCertification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.certification.name}"

class MetricsReport(models.Model):
    year = models.IntegerField(unique=True)
    courses_completed = models.IntegerField(default=0)
    certifications = models.IntegerField(default=0)
    employees_trained = models.IntegerField(default=0)
    interns = models.IntegerField(default=0)
    intern_projects = models.IntegerField(default=0)
    sme_sessions = models.IntegerField(default=0)

    def __str__(self):
        return f"Metrics for {self.year}"
