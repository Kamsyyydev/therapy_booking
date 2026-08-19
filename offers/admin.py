from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'offer_type', 'price', 'duration_minutes', 'sessions_included', 'is_student_offer', 'badge', 'is_active')
    list_filter = ('category', 'offer_type', 'is_student_offer', 'is_active')
    search_fields = ('name', 'description', 'tagline', 'badge')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'badge', 'is_active')
    fields = ('name', 'slug', 'category', 'offer_type', 'price', 'discounted_price', 'is_student_offer', 'duration_minutes', 'sessions_included', 'badge', 'tagline', 'description', 'features', 'image', 'is_active', 'display_order')
