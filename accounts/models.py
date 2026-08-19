from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TherapistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist_profile')
    title = models.CharField(max_length=150, default='Licensed Clinical Psychologist')
    specialization = models.CharField(max_length=255, default='Anxiety, Depression, Trauma, Life Transitions')
    bio = models.TextField(blank=True, default='Compassionate, evidence-based therapy tailored to your unique journey.')
    photo = models.ImageField(upload_to='therapists/', null=True, blank=True, help_text='Profile photo')
    photo_url = models.URLField(blank=True, default='', help_text='External image link or static path if not uploading')
    avatar_color = models.CharField(max_length=20, default='#5B9EA7')
    availability = models.JSONField(default=dict, blank=True, help_text='e.g. {"monday": "9-5", "tuesday": "9-5"}')
    is_accepting_clients = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name() or self.user.username}"

    def get_display_name(self):
        return self.user.get_full_name() or self.user.username

    def get_initials(self):
        name = self.get_display_name()
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return name[:2].upper()

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        if self.photo_url:
            return self.photo_url
        return None

class StudentVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_verification')
    edu_email = models.EmailField(unique=True, help_text='Must end in .edu, .edu.ng, or university domain')
    school_name = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = 'Verified' if self.is_verified else 'Pending'
        return f"{self.user.username} ({self.edu_email}) - {status}"

    def verify_if_eligible(self):
        email = self.edu_email.strip().lower()
        if (email.endswith('.edu') or 
            email.endswith('.edu.ng') or 
            email.endswith('.sch.ng') or 
            email.endswith('.ac.uk') or 
            '.edu.' in email):
            self.is_verified = True
            self.verified_at = timezone.now()
            self.save()
            return True
        return False
