from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Department

class Command(BaseCommand):
    help = 'Create a superuser and default department'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create default department if it doesn't exist
        department, created = Department.objects.get_or_create(
            id=1,  # Make sure it has ID=1 as referenced in the code
            defaults={
                'name': 'Default Department'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created default department: {department.name}'))

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin123',
                first_name='Admin',
                last_name='User',
                designation=department
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
