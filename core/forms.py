from django import forms
from .models import User, Department, Profile
from django.core.exceptions import ValidationError

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'contact_no', 'About', 'Date_of_birth', 'profile_picture')
        widgets = {
            'Date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = "Username*"
        
class ProfessionalDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('emp_id', 'designation', 'expertise', 'email', 'Date_of_joining')
        widgets = {
            'Date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = "Email*"
        self.fields['designation'].required = False  # Make designation optional

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'department', 'About')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'Date_of_birth', 'Date_of_joining', 'emp_id', 'About', 'profile_picture', 'designation', 'contact_no', 'expertise', 'certifications', 'department')
    designation = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserUpdationForm(forms.ModelForm):
    """
    Form to handle user profile updates.

    Attributes:
        department (ModelChoiceField): A field to select the user's department.
    """
    department = forms.ModelChoiceField(queryset=Department.objects.filter(parent=None))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'emp_id', 'designation', 
                  'Date_of_birth', 'contact_no', 'expertise', 'certifications', 
                  'Date_of_joining', 'department', 'About']
        widgets = {
            'Date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'Date_of_joining': forms.DateInput(attrs={'type': 'date'})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'parent']
