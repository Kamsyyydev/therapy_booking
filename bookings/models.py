from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from offers.models import Offer

class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Confirmation'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    therapist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='therapist_sessions',
        help_text='Assigned therapist or counselor'
    )
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='bookings')
    
    start_time = models.DateTimeField(null=True, blank=True, help_text='Session appointment start date and time')
    end_time = models.DateTimeField(null=True, blank=True, help_text='Auto-calculated based on offer duration')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)
    client_notes = models.TextField(blank=True, help_text='Special requests or focus areas from the client')
    meeting_link = models.URLField(blank=True, default='', help_text='Virtual room or clinic location info')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time', '-created_at']

    def __str__(self):
        therapist_name = self.therapist.get_full_name() if self.therapist else 'Unassigned'
        return f"{self.offer.name} for {self.client.username} with {therapist_name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Automatically calculate end_time based on offer duration if start_time is set
        if self.start_time and not self.end_time:
            duration = self.offer.duration_minutes or 50
            self.end_time = self.start_time + timedelta(minutes=duration)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        if not self.start_time:
            return True
        return self.start_time >= timezone.now() and self.status in [self.STATUS_PENDING, self.STATUS_CONFIRMED]

    @property
    def is_past(self):
        if not self.start_time:
            return False
        return self.start_time < timezone.now() or self.status in [self.STATUS_COMPLETED, self.STATUS_CANCELLED]
