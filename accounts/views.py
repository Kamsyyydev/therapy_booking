from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CustomUserCreationForm, StudentVerificationForm
from .models import StudentVerification, TherapistProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('offers:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            role = form.cleaned_data.get('role', 'client')
            is_student = form.cleaned_data.get('is_student', False)

            if role == 'therapist':
                TherapistProfile.objects.create(
                    user=user,
                    title='Licensed Mental Health Counselor',
                    specialization='Anxiety, CBT, Stress Management',
                    availability={'monday': '9-5', 'tuesday': '9-5', 'wednesday': '9-5', 'thursday': '9-5', 'friday': '9-4'}
                )
            
            # If user entered a .edu / .edu.ng email or checked student, initialize verification
            email_lower = user.email.lower()
            is_academic_email = (
                email_lower.endswith('.edu') or
                email_lower.endswith('.edu.ng') or
                email_lower.endswith('.sch.ng') or
                email_lower.endswith('.ac.uk') or
                '.edu.' in email_lower
            )

            if is_student or is_academic_email:
                sv = StudentVerification.objects.create(
                    user=user,
                    edu_email=user.email,
                    school_name=''
                )
                if is_academic_email:
                    sv.is_verified = True
                    sv.verified_at = timezone.now()
                    sv.save()

            login(request, user)
            messages.success(request, f'Welcome to Serenity Haven, {user.first_name}! Your account is ready.')
            
            if role == 'therapist':
                return redirect('bookings:therapist_dashboard')
            return redirect('bookings:client_dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('offers:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f'Welcome back, {user.first_name or user.username}!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if hasattr(user, 'therapist_profile'):
                return redirect('bookings:therapist_dashboard')
            return redirect('bookings:client_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been successfully logged out. Take care!')
    return redirect('offers:home')

@login_required
def verify_student_view(request):
    student_verification = getattr(request.user, 'student_verification', None)
    
    if request.method == 'POST':
        form = StudentVerificationForm(request.POST, instance=student_verification)
        if form.is_valid():
            sv = form.save(commit=False)
            sv.user = request.user
            sv.is_verified = True
            sv.verified_at = timezone.now()
            sv.save()
            messages.success(request, 'Congratulations! Your student status is verified. All student discounts unlocked!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('offers:home')
    else:
        initial = {'edu_email': request.user.email} if request.user.email else {}
        form = StudentVerificationForm(instance=student_verification, initial=initial)
    
    return render(request, 'accounts/verify_student.html', {
        'form': form,
        'student_verification': student_verification
    })
