from django.contrib import admin
from .models import Course, Certification, UserEnrollment, UserCertification, MetricsReport

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'progress', 'points', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    list_filter = ('created_at', 'updated_at', 'points')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'progress', 'points', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    list_filter = ('created_at', 'updated_at', 'points')

@admin.register(UserEnrollment)
class UserEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'certification', 'course_progress', 'certification_progress')
    search_fields = ('user__username', 'course__name', 'certification__name')

@admin.register(UserCertification)
class UserCertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'certification', 'enrolled_at', 'completed_at')
    search_fields = ('user__username', 'certification__name')
    list_filter = ('enrolled_at', 'completed_at')

@admin.register(MetricsReport)
class MetricsReportAdmin(admin.ModelAdmin):
    list_display = ('year', 'courses_completed', 'certifications', 'employees_trained', 'interns')
    search_fields = ('year',)
    list_filter = ('year',)
