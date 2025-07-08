import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JET.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def create_test_user():
    """Create a test user with known credentials."""
    
    username = "testuser123"
    email = "testuser123@example.com"
    password = "Test@12345"
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"Reset password for existing user: {username}")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="Test",
            last_name="User"
        )
        print(f"Created new test user: {username}")
    
    print("\n----- TEST USER CREDENTIALS -----")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("---------------------------------\n")
    
    return user

if __name__ == "__main__":
    create_test_user()
