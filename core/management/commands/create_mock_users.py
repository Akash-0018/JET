from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department, Profile
from django.utils import timezone
from datetime import timedelta
import random
from django.core.files.base import ContentFile
import os
import requests
from io import BytesIO

User = get_user_model()

class Command(BaseCommand):
    help = 'Create 10 mock users with profiles'

    def handle(self, *args, **kwargs):
        # Create default department if it doesn't exist
        department, created = Department.objects.get_or_create(name='Engineering')
        if created:
            self.stdout.write(self.style.SUCCESS('Created default department: Engineering'))
        
        # Create more departments for variety
        departments = [department]
        for dept_name in ['Marketing', 'Finance', 'HR', 'Sales', 'IT']:
            dept, created = Department.objects.get_or_create(name=dept_name)
            departments.append(dept)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {dept_name}'))

        # Expertise options
        expertise_options = [
            'Python, Django, REST API',
            'Java, Spring Boot, Microservices',
            'JavaScript, React, Node.js',
            'Data Science, Machine Learning, AI',
            'DevOps, CI/CD, AWS',
            'Project Management, Agile, Scrum',
            'UI/UX Design, Figma, Adobe XD',
            'Content Writing, SEO, Digital Marketing',
            'Financial Analysis, Accounting',
            'HR Management, Recruitment'
        ]

        # Create 10 mock users
        for i in range(1, 11):
            try:
                # Generate random data
                first_name = f'User{i}'
                last_name = f'Test{i}'
                username = f'testuser{i}'
                email = f'testuser{i}@example.com'
                emp_id = f'EMP{1000+i}'
                designation = random.choice(departments)
                dob = timezone.now().date() - timedelta(days=random.randint(8000, 15000))  # Random age between ~22-40
                joining_date = timezone.now().date() - timedelta(days=random.randint(30, 1825))  # Between 1 month to 5 years
                expertise = random.choice(expertise_options)
                about = f"This is a mock user {i} created for testing purposes."
                contact_no = f'98765{43210+i}'[-10:]

                # Create or update user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'emp_id': emp_id,
                        'designation': designation,
                        'Date_of_birth': dob,
                        'Date_of_joining': joining_date,
                        'expertise': expertise,
                        'About': about,
                        'contact_no': contact_no,
                        'is_staff': False,
                        'is_active': True,
                    }
                )

                # Set password
                if created:
                    user.set_password('password123')
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'User {username} already exists, updating details'))
                    # Update existing user
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.emp_id = emp_id
                    user.designation = designation
                    user.Date_of_birth = dob
                    user.Date_of_joining = joining_date
                    user.expertise = expertise
                    user.About = about
                    user.contact_no = contact_no
                    user.save()

                # Create or update profile
                try:
                    profile = Profile.objects.get(user=user)
                    self.stdout.write(self.style.WARNING(f'Profile for {username} already exists, updating'))
                except Profile.DoesNotExist:
                    profile = Profile(user=user)
                    self.stdout.write(self.style.SUCCESS(f'Creating profile for {username}'))

                profile.department = designation
                profile.About = about
                profile.score = random.randint(0, 1000)  # Random score for games
                profile.last_login_time = timezone.now() - timedelta(days=random.randint(0, 30))
                
                # Try to get a random avatar image
                try:
                    # Get random avatar
                    avatar_id = random.randint(1, 70)
                    response = requests.get(f'https://i.pravatar.cc/300?img={avatar_id}')
                    if response.status_code == 200:
                        img_temp = BytesIO(response.content)
                        file_name = f'avatar_{username}.jpg'
                        profile.profile_picture.save(file_name, ContentFile(img_temp.getvalue()), save=False)
                        self.stdout.write(self.style.SUCCESS(f'Added profile picture for {username}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding profile picture: {e}'))
                
                profile.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {i}: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully created mock users'))
