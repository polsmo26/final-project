from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, StudentProfile
from datetime import date

class StudentRegistrationForm(UserCreationForm):
    school = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your school Name'
        })
    )
    grade_level = forms.ChoiceField(
        choices=[
            ('', 'Select Grade Level'),
            ('9', '9th Grade'),
            ('10', '10th Grade'),
            ('11', '11th Grade'),
            ('12', '12th Grade'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    town = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Town'
        })
    )
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': date.today().strftime('%Y-%m-%d')
        }),
        label="Birthday (optional)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2', 
                 'school', 'grade_level', 'town', 'birthdate']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            'class': 'form-control',
            'placeholder': None
        }
        
        placeholders = {
            'username': 'Choose a username...',
            'password1': 'Create a password...',
            'password2': 'Confirm your password',
        }
        
        for field_name, field in self.fields.items():
            if field_name in placeholders:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholders[field_name]
                })
            elif not field.widget.attrs.get('class'):
                field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_student = True
        
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                school=self.cleaned_data['school'],
                grade_level=self.cleaned_data['grade_level'],
                town=self.cleaned_data['town'],
                birthdate=self.cleaned_data['birthdate'],
            )
        return user

class StudentProfileEditForm(forms.ModelForm):
    GRADE_LEVEL_CHOICES = [
        ('', 'Select Grade Level'),
        ('9', '9th Grade'),
        ('10', '10th Grade'),
        ('11', '11th Grade'),
        ('12', '12th Grade'),
    ]
    grade_level = forms.ChoiceField(
        choices=GRADE_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    class Meta:
        model = StudentProfile
        fields = ['school', 'grade_level', 'town', 'birthdate', 'parent_contact']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your school name'
        })
        self.fields['town'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your town'
        })
        self.fields['birthdate'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',
            'max': date.today().strftime('%Y-%m-%d')
        })
        self.fields['parent_contact'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Parent/guardian contact'
        })
        
        self.fields['birthdate'].label = "Birthday (optional)"
        self.fields['parent_contact'].required = False
        