from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Profile, Intern, SMEdetails

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'About', 'profile_picture',
                                     'Date_of_birth', 'contact_no')}),
        ('Professional info', {'fields': ('emp_id', 'designation', 'expertise', 'certifications',
                                         'Date_of_joining', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
admin.site.register(User, CustomUserAdmin)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'score', 'last_login_time')
    search_fields = ('user__username', 'user__email')
    
@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('intern_name', 'intern_role', 'college', 'start_date', 'end_date')
    search_fields = ('intern_name', 'college', 'project_worked')
    
@admin.register(SMEdetails)
class SMEdetailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'duration', 'handled_by', 'audience')
    search_fields = ('title', 'handled_by__username')
