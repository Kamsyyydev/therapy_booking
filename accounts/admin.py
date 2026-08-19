from django.contrib import admin
from .models import TherapistProfile, StudentVerification

@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'specialization', 'is_accepting_clients', 'created_at')
    list_filter = ('is_accepting_clients', 'title')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    fields = ('user', 'title', 'specialization', 'bio', 'photo', 'photo_url', 'avatar_color', 'availability', 'is_accepting_clients')

@admin.register(StudentVerification)
class StudentVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'edu_email', 'school_name', 'is_verified', 'verified_at')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'edu_email', 'school_name')
