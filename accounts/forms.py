from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentVerification, TherapistProfile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Your given name')
    last_name = forms.CharField(max_length=50, required=True, help_text='Your family name')
    email = forms.EmailField(required=True, help_text='Primary email address')
    is_student = forms.BooleanField(required=False, initial=False, label='I am a student (unlock discounted student offers)')
    role = forms.ChoiceField(
        choices=[('client', 'Client / Individual'), ('therapist', 'Therapist / Counselor')],
        initial='client',
        widget=forms.RadioSelect,
        label='I am signing up as a'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_student')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['role', 'is_student']:
                field.widget.attrs.update({'class': 'form-control'})
            elif field_name == 'is_student':
                field.widget.attrs.update({'class': 'form-check-input me-2'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

class StudentVerificationForm(forms.ModelForm):
    class Meta:
        model = StudentVerification
        fields = ('edu_email', 'school_name')
        widgets = {
            'edu_email': forms.EmailInput(attrs={'placeholder': 'e.g. yourname@futo.edu.ng or student@unilag.edu.ng', 'class': 'form-control form-control-lg'}),
            'school_name': forms.TextInput(attrs={'placeholder': 'e.g. Federal University of Technology, Owerri (FUTO), IMSU, UNILAG', 'class': 'form-control form-control-lg'}),
        }

    def clean_edu_email(self):
        email = self.cleaned_data.get('edu_email', '').strip().lower()
        if not (email.endswith('.edu') or 
                email.endswith('.edu.ng') or 
                email.endswith('.sch.ng') or 
                email.endswith('.ac.uk') or 
                '.edu.' in email):
            raise forms.ValidationError('Email must end with .edu, .edu.ng, or a recognized academic institution domain.')
        return email
