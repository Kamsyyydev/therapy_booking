from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('offer', 'client', 'therapist', 'start_time', 'status', 'created_at')
    list_filter = ('status', 'start_time', 'created_at', 'offer__category')
    search_fields = ('client__username', 'client__email', 'therapist__username', 'offer__name')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)
