from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .models import User, Department, Profile, Intern, SMEdetails
from .forms import PersonalDetailsForm, ProfessionalDetailsForm, DepartmentForm, UserRegistrationForm, UserUpdationForm
from learning.models import UserEnrollment, UserCertification

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        # Instantiate forms with POST data and possible file uploads
        user_registration_form = UserRegistrationForm(request.POST)
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES)  # Include request.FILES
        professional_details_form = ProfessionalDetailsForm(request.POST)

        # Check if all forms are valid
        if user_registration_form.is_valid() and personal_details_form.is_valid() and professional_details_form.is_valid():
            # Create a new user
            user = user_registration_form.save(commit=False)  # Don't save to DB yet
            user.designation = Department.objects.get(id=1)  # Assuming 1 is the ID of a default department
            user.save()  # Save the user

            # Save the profile picture
            profile = Profile(user=user)  # Create a new Profile instance for the user
            profile.profile_picture = personal_details_form.cleaned_data['profile_picture']
            profile.save()  # Save the profile

            # Update the personal details
            personal_details_form.instance = user  # Assign the user instance to the form
            personal_details_form.save()  # Save personal details

            # Update the professional details
            professional_details_form.instance = user  # Assign the user instance to the form
            professional_details_form.save()  # Save professional details
            
            # Login the user
            login(request, user)

            # Redirect to the user's dashboard
            return redirect('dashboard')  # Redirecting to the dashboard using the URL name
            
        else:
            # If there are errors, render the form with errors
            return render(request, 'register.html', {
                'user_registration_form': user_registration_form,
                'personal_details_form': personal_details_form,
                'professional_details_form': professional_details_form,
            })
    else:
        # If not a POST request, instantiate empty forms
        user_registration_form = UserRegistrationForm()
        personal_details_form = PersonalDetailsForm()
        professional_details_form = ProfessionalDetailsForm()
        return render(request, 'register.html', {
            'user_registration_form': user_registration_form,
            'personal_details_form': personal_details_form,
            'professional_details_form': professional_details_form,
        })

def login_view(request):
    if request.method == 'POST':
        # Check if the username and password fields are present in the request
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Pass the user object to the login function
                login(request, user)
                # Redirect based on user type
                return redirect('dashboard')
            else:
                # Display error if authentication fails
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            # If username or password is not in the request, display an error
            error_message = 'Both username and password are required.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request, pk=None):
    if pk:
        user = get_object_or_404(User, pk=pk)
    else:
        user = request.user

    # Fetch all the necessary data for the dashboard
    # Get user enrollments with course data
    enrolled_courses = UserEnrollment.objects.filter(
        user=user,
        course__isnull=False
    ).select_related('course')
    
    # Get user enrollments with certification data
    certifications = UserEnrollment.objects.filter(
        user=user,
        certification__isnull=False
    ).select_related('certification')
    
    context = {
        'user': user,
        'enrolled_courses': enrolled_courses,
        'certifications': certifications,
    }

    return render(request, 'dashboard.html', context)


def user_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'user_list.html', context)


def user_detail(request, pk):
    from learning.models import UserEnrollment, UserCertification, Course
    from django.db.models import Sum, Count
    
    user = get_object_or_404(User, pk=pk)
    
    # Get user's enrolled courses
    enrolled_courses = UserEnrollment.objects.filter(
        user=user,
        course__isnull=False
    ).select_related('course').order_by('-course_enrolled_at')
      # Get user's certifications
    certifications = UserCertification.objects.filter(
        user=user
    ).select_related('certification').order_by('-enrolled_at')
    
    # Get user's enrollments that are in progress
    in_progress_enrollments = UserEnrollment.objects.filter(
        user=user,
        course_progress__lt=100,
        course_progress__gt=0
    ).order_by('-course_enrolled_at')
    
    # Get user's completed enrollments
    completed_enrollments = UserEnrollment.objects.filter(
        user=user,
        course_progress=100
    ).order_by('-course_completed_at')
      # Calculate total points
    points = 0
    for enrollment in enrolled_courses:
        if enrollment.course:
            try:
                points += int(enrollment.course.points)
            except (ValueError, TypeError):
                pass
    
    # Add points from profile if available
    if hasattr(user, 'profile') and user.profile:
        try:
            points += user.profile.score
        except (AttributeError, TypeError):
            pass
    
    # Get enrollment statistics
    total_courses = enrolled_courses.count()
    completed_courses = completed_enrollments.count()
    in_progress_courses = in_progress_enrollments.count()
    
    # Calculate completion percentage
    completion_percentage = 0
    if total_courses > 0:
        completion_percentage = int((completed_courses / total_courses) * 100)
    
    context = {
        'user': user,
        'enrolled_courses': enrolled_courses,
        'certifications': certifications,
        'in_progress_enrollments': in_progress_enrollments,
        'completed_enrollments': completed_enrollments,
        'total_courses': total_courses,
        'completed_courses': completed_courses, 
        'in_progress_courses': in_progress_courses,
        'completion_percentage': completion_percentage,
        'points': points,
    }
    return render(request, 'user_detail.html', context)

@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Ensure that the user can only update their own profile unless they are staff
    if request.user != user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this profile.")
        return HttpResponseForbidden()

    if request.method == 'POST':
        # Create forms with the incoming POST data
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES, instance=user)
        professional_details_form = ProfessionalDetailsForm(request.POST, instance=user)

        if personal_details_form.is_valid() and professional_details_form.is_valid():
            try:
                # Update user's profile with cleaned data from forms
                user = personal_details_form.save(commit=False)  # Get the user instance

                # Update personal details
                user.username = personal_details_form.cleaned_data.get('username')
                user.first_name = personal_details_form.cleaned_data.get('first_name')
                user.last_name = personal_details_form.cleaned_data.get('last_name')
                if 'Date_of_birth' in personal_details_form.cleaned_data:
                    user.Date_of_birth = personal_details_form.cleaned_data.get('Date_of_birth')
                user.save()  # Save changes to user

                # Handle the profile picture if provided
                if 'profile_picture' in request.FILES:
                    user.profile_picture = request.FILES['profile_picture']
                    user.save()

                # Update professional details
                if 'emp_id' in professional_details_form.cleaned_data:
                    user.emp_id = professional_details_form.cleaned_data.get('emp_id')
                if 'designation' in professional_details_form.cleaned_data:
                    user.designation = professional_details_form.cleaned_data.get('designation')
                if 'expertise' in professional_details_form.cleaned_data:
                    user.expertise = professional_details_form.cleaned_data.get('expertise')
                if 'Date_of_joining' in professional_details_form.cleaned_data:
                    user.Date_of_joining = professional_details_form.cleaned_data.get('Date_of_joining')
                
                # Save professional details
                professional_details_form.save()

                # Add success message
                messages.success(request, f"Profile for {user.get_full_name() or user.username} has been updated successfully!")
                
                # Redirect to the user's detail page
                return redirect('user_detail', pk=user.pk)
            
            except Exception as e:
                messages.error(request, f"An error occurred while updating the profile: {str(e)}")
        else:
            # Form validation failed
            for form in [personal_details_form, professional_details_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            messages.error(request, "Please correct the errors in the form.")
    else:
        # If not a POST request, render forms with the current user's data
        personal_details_form = PersonalDetailsForm(instance=user)
        professional_details_form = ProfessionalDetailsForm(instance=user)

    # Provide the forms to the template
    context = {
        'personal_details_form': personal_details_form,
        'professional_details_form': professional_details_form,
        'user': user,
        'form': personal_details_form,  # Include original form for backwards compatibility
    }
    
    return render(request, 'user_update.html', context)

def get_sub_departments(request, department_id):
    sub_departments = Department.objects.filter(parent_id=department_id)
    data = [{'id': dept.id, 'name': dept.name} for dept in sub_departments]
    return JsonResponse(data, safe=False)

@login_required
def leaderboard(request):
    from learning.models import Course, Certification, UserEnrollment, UserCertification
    from django.db.models import Count
    
    # Get users with their course and certification counts
    user_stats = []
    
    users = User.objects.all()
    for user in users:
        user_courses = UserEnrollment.objects.filter(user=user, course__isnull=False, course_completed_at__isnull=False)
        user_certifications = UserCertification.objects.filter(user=user, completed_at__isnull=False)
          # Get course and certification details
        courses_data = []
        for uc in user_courses:
            courses_data.append({
                'name': uc.course.name,
                'date_completed': uc.course_completed_at
            })
            
        certifications_data = []
        for cert in user_certifications:
            certifications_data.append({
                'name': cert.certification.name,
                'date_completed': cert.completed_at
            })
        
        # Sort by completion date, most recent first
        courses_data.sort(key=lambda x: x['date_completed'] if x['date_completed'] else '1900-01-01', reverse=True)
        certifications_data.sort(key=lambda x: x['date_completed'] if x['date_completed'] else '1900-01-01', reverse=True)
        
        # Create user entry
        user_entry = {
            'username': user.username,
            'user_id': user.id,
            'num_courses': len(user_courses),
            'num_certifications': len(user_certifications),
            'courses': courses_data,
            'certifications': certifications_data,
            'total_achievements': len(user_courses) + len(user_certifications)
        }
        
        user_stats.append(user_entry)
    
    # Sort by total achievements
    user_stats.sort(key=lambda x: x['total_achievements'], reverse=True)
    
    # Add rank
    leaderboard = []
    for i, entry in enumerate(user_stats):
        entry['rank'] = i + 1
        leaderboard.append(entry)
    
    context = {
        'leaderboard': leaderboard
    }
    
    return render(request, 'leaderboard.html', context)

@login_required
def update_user_score(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        score = request.POST.get('score')
        
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            profile.score = score
            profile.save()
            return JsonResponse({'success': True})
        except (User.DoesNotExist, Profile.DoesNotExist) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Get user profiles with scores ordered by descending score
    profiles = Profile.objects.select_related('user').all().order_by('-score')
    
    # Create leaderboard data with ranks
    leaderboard = []
    for i, profile in enumerate(profiles):
        user_entry = {
            'rank': i + 1,
            'username': profile.user.username,
            'score': profile.score or 0,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None
        }
        leaderboard.append(user_entry)
    
    return render(request, 'leaderboard1.html', {'leaderboard': leaderboard})

@login_required
def help(request):
    return render(request, 'help.html')
