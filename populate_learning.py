import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JET.settings')
django.setup()

from django.contrib.auth import get_user_model
from learning.models import Course, Certification, UserEnrollment, UserCertification, MetricsReport
from core.models import SMEdetails
from django.utils import timezone

User = get_user_model()

def create_courses():
    """Create 10 courses with different details."""
    courses = [
        {
            'name': 'Introduction to Python Programming',
            'description': 'Learn the basics of Python programming language including syntax, data types, and control structures.',
            'link': 'https://example.com/courses/python-intro',
            'points': '3'
        },
        {
            'name': 'Advanced JavaScript Development',
            'description': 'Master advanced JavaScript concepts including closures, promises, async/await, and modern ES6+ features.',
            'link': 'https://example.com/courses/advanced-js',
            'points': '4'
        },
        {
            'name': 'Data Science Fundamentals',
            'description': 'Introduction to data science concepts, tools, and methodologies with practical examples.',
            'link': 'https://example.com/courses/data-science',
            'points': '4'
        },
        {
            'name': 'Machine Learning Basics',
            'description': 'Learn the foundations of machine learning algorithms and their applications.',
            'link': 'https://example.com/courses/ml-basics',
            'points': '5'
        },
        {
            'name': 'Cloud Computing with AWS',
            'description': 'Comprehensive guide to AWS services and cloud architecture design patterns.',
            'link': 'https://example.com/courses/aws-cloud',
            'points': '4'
        },
        {
            'name': 'DevOps and CI/CD Pipelines',
            'description': 'Learn to implement continuous integration and deployment pipelines using modern DevOps tools.',
            'link': 'https://example.com/courses/devops-cicd',
            'points': '3'
        },
        {
            'name': 'Web Development with Django',
            'description': 'Build robust web applications using the Django framework and best practices.',
            'link': 'https://example.com/courses/django-web',
            'points': '3'
        },
        {
            'name': 'Mobile App Development with Flutter',
            'description': 'Create cross-platform mobile applications using Flutter and Dart programming language.',
            'link': 'https://example.com/courses/flutter-mobile',
            'points': '4'
        },
        {
            'name': 'Database Design and SQL',
            'description': 'Master database design principles and SQL for effective data management.',
            'link': 'https://example.com/courses/database-sql',
            'points': '3'
        },
        {
            'name': 'Cybersecurity Essentials',
            'description': 'Learn essential cybersecurity concepts and best practices for protecting systems and data.',
            'link': 'https://example.com/courses/cybersecurity',
            'points': '5'
        }
    ]
    
    created_courses = []
    users = list(User.objects.all())
    
    if not users:
        print("No users found in the database. Please create users first.")
        return []
    
    for course_data in courses:
        # Assign a random user as the course creator
        random_user = random.choice(users)
        
        # Create course with random progress
        course = Course.objects.create(
            name=course_data['name'],
            description=course_data['description'],
            link=course_data['link'],
            points=course_data['points'],
            user=random_user,
            progress=random.randint(0, 100)
        )
        created_courses.append(course)
        print(f"Created course: {course.name}")
    
    return created_courses

def create_certifications():
    """Create 10 certifications with different details."""
    certifications = [
        {
            'name': 'AWS Certified Solutions Architect',
            'description': 'Professional certification for designing distributed systems on AWS.',
            'link': 'https://example.com/certifications/aws-architect',
            'points': '5'
        },
        {
            'name': 'Microsoft Certified: Azure Developer Associate',
            'description': 'Certification for developing solutions using Microsoft Azure services.',
            'link': 'https://example.com/certifications/azure-developer',
            'points': '4'
        },
        {
            'name': 'Google Professional Data Engineer',
            'description': 'Certification for designing and building data processing systems on Google Cloud.',
            'link': 'https://example.com/certifications/gcp-data-engineer',
            'points': '5'
        },
        {
            'name': 'Certified Kubernetes Administrator (CKA)',
            'description': 'Certification for Kubernetes administration and deployment expertise.',
            'link': 'https://example.com/certifications/kubernetes-admin',
            'points': '4'
        },
        {
            'name': 'Certified Ethical Hacker (CEH)',
            'description': 'Certification for network security professionals specialized in ethical hacking.',
            'link': 'https://example.com/certifications/ethical-hacker',
            'points': '5'
        },
        {
            'name': 'Cisco Certified Network Associate (CCNA)',
            'description': 'Certification for implementing and administering Cisco networking solutions.',
            'link': 'https://example.com/certifications/cisco-ccna',
            'points': '3'
        },
        {
            'name': 'CompTIA Security+',
            'description': 'Certification that validates baseline cybersecurity skills.',
            'link': 'https://example.com/certifications/comptia-security',
            'points': '3'
        },
        {
            'name': 'Oracle Certified Professional: Java Developer',
            'description': 'Certification for Java programming language expertise.',
            'link': 'https://example.com/certifications/oracle-java',
            'points': '4'
        },
        {
            'name': 'Salesforce Certified Administrator',
            'description': 'Certification for professionals who implement, configure and manage Salesforce.',
            'link': 'https://example.com/certifications/salesforce-admin',
            'points': '3'
        },
        {
            'name': 'PMI Project Management Professional (PMP)',
            'description': 'Certification for project management professionals demonstrating expertise.',
            'link': 'https://example.com/certifications/pmi-pmp',
            'points': '5'
        }
    ]
    
    created_certifications = []
    users = list(User.objects.all())
    
    if not users:
        print("No users found in the database. Please create users first.")
        return []
    
    for cert_data in certifications:
        # Assign a random user as the certification creator
        random_user = random.choice(users)
        
        # Create certification with random progress
        certification = Certification.objects.create(
            name=cert_data['name'],
            description=cert_data['description'],
            link=cert_data['link'],
            points=cert_data['points'],
            user=random_user,
            progress=random.randint(0, 100)
        )
        created_certifications.append(certification)
        print(f"Created certification: {certification.name}")
    
    return created_certifications

def create_user_enrollments(courses, certifications):
    """Create user enrollments for courses and certifications."""
    users = list(User.objects.all())
    
    if not users:
        print("No users found in the database. Please create users first.")
        return
    
    # For each user, randomly assign some courses and certifications
    for user in users:
        # Randomly decide how many courses (0-3) this user will be enrolled in
        num_courses = random.randint(0, 3)
        if num_courses > 0 and courses:
            # Select random courses for this user
            selected_courses = random.sample(courses, min(num_courses, len(courses)))
            for course in selected_courses:
                # Randomly determine if course is completed
                is_completed = random.choice([True, False])
                progress = 100 if is_completed else random.randint(10, 90)
                
                # Calculate enrollment and completion dates
                now = timezone.now()
                enrolled_at = now - timedelta(days=random.randint(30, 365))
                completed_at = now - timedelta(days=random.randint(1, 29)) if is_completed else None
                
                # Create enrollment
                UserEnrollment.objects.create(
                    user=user,
                    course=course,
                    course_enrolled_at=enrolled_at,
                    course_completed_at=completed_at,
                    course_progress=progress
                )
                print(f"Enrolled user {user.username} in course {course.name}")
        
        # Randomly decide how many certifications (0-2) this user will pursue
        num_certs = random.randint(0, 2)
        if num_certs > 0 and certifications:
            # Select random certifications for this user
            selected_certs = random.sample(certifications, min(num_certs, len(certifications)))
            for cert in selected_certs:
                # Randomly determine if certification is completed
                is_completed = random.choice([True, False])
                progress = 100 if is_completed else random.randint(10, 90)
                
                # Calculate enrollment and completion dates
                now = timezone.now()
                enrolled_at = now - timedelta(days=random.randint(30, 365))
                completed_at = now - timedelta(days=random.randint(1, 29)) if is_completed else None
                
                # Create enrollment
                enrollment = UserEnrollment.objects.create(
                    user=user,
                    certification=cert,
                    certification_enrolled_at=enrolled_at,
                    certification_completed_at=completed_at,
                    certification_progress=progress
                )
                
                # Also create a UserCertification if completed
                if is_completed:
                    UserCertification.objects.create(
                        user=user,
                        certification=cert,
                        enrolled_at=enrolled_at,
                        completed_at=completed_at
                    )
                
                print(f"Enrolled user {user.username} in certification {cert.name}")

def update_metrics_report():
    """Update the metrics report with the newly created data."""
    current_year = datetime.now().year
    
    # Count data for the report
    courses_completed = UserEnrollment.objects.filter(
        course_completed_at__isnull=False, 
        course_completed_at__year=current_year
    ).count()
    
    certifications_completed = UserCertification.objects.filter(
        completed_at__isnull=False,
        completed_at__year=current_year
    ).count()
    
    # Get unique users who have completed a course or certification this year
    unique_users_with_courses = UserEnrollment.objects.filter(
        course_completed_at__isnull=False, 
        course_completed_at__year=current_year
    ).values_list('user', flat=True).distinct()
    
    unique_users_with_certs = UserCertification.objects.filter(
        completed_at__isnull=False,
        completed_at__year=current_year
    ).values_list('user', flat=True).distinct()
    
    # Combine and get unique count
    employees_trained = len(set(list(unique_users_with_courses) + list(unique_users_with_certs)))
    
    # Count interns
    interns = User.objects.filter(intern__isnull=False).count()
    
    # Count intern projects (assuming one project per intern)
    intern_projects = User.objects.filter(
        intern__isnull=False, 
        intern__project_worked__isnull=False
    ).count()
    
    # Count SME sessions
    sme_sessions = SMEdetails.objects.filter(
        date__year=current_year
    ).count()
    
    # Create or update the metrics report
    metrics, created = MetricsReport.objects.get_or_create(
        year=current_year,
        defaults={
            'courses_completed': courses_completed,
            'certifications': certifications_completed,
            'employees_trained': employees_trained,
            'interns': interns,
            'intern_projects': intern_projects,
            'sme_sessions': sme_sessions
        }
    )
    
    if not created:
        metrics.courses_completed = courses_completed
        metrics.certifications = certifications_completed
        metrics.employees_trained = employees_trained
        metrics.interns = interns
        metrics.intern_projects = intern_projects
        metrics.sme_sessions = sme_sessions
        metrics.save()
    
    print(f"Updated metrics report for {current_year}")

def main():
    print("Starting to populate learning data...")
    
    # Delete existing data to avoid duplicates
    print("Deleting existing learning data...")
    Course.objects.all().delete()
    Certification.objects.all().delete()
    UserEnrollment.objects.all().delete()
    UserCertification.objects.all().delete()
    
    # Create courses and certifications
    courses = create_courses()
    certifications = create_certifications()
    
    # Create user enrollments
    create_user_enrollments(courses, certifications)
    
    # Update metrics report
    update_metrics_report()
    
    print("Database population completed successfully!")

if __name__ == "__main__":
    main()
