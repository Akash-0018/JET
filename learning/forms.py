from django import forms
from .models import Course, Certification, UserCertification, UserEnrollment

class UserCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'link', 'progress', 'points']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserCertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'description', 'link', 'progress', 'points']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
