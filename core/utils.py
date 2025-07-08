from django.utils import timezone

def update_last_login_time(user):
    """
    Update the user's last login time in their profile
    """
    try:
        profile = user.profile
        profile.last_login_time = timezone.now()
        profile.save()
    except:
        # If profile doesn't exist, just pass
        pass
        
def get_department_hierarchy():
    """
    Returns a dictionary with department hierarchies
    """
    from .models import Department
    
    departments = Department.objects.all()
    hierarchy = {}
    
    # Get all root departments (no parent)
    root_departments = departments.filter(parent=None)
    
    for dept in root_departments:
        hierarchy[dept] = get_sub_departments(dept)
    
    return hierarchy

def get_sub_departments(department):
    """
    Recursively gets all sub-departments for a given department
    """
    from .models import Department
    
    sub_departments = {}
    children = Department.objects.filter(parent=department)
    
    for child in children:
        sub_departments[child] = get_sub_departments(child)
    
    return sub_departments
