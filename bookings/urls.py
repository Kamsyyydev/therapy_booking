from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<slug:slug>/', views.book_offer_view, name='book_offer'),
    path('dashboard/', views.client_dashboard_view, name='client_dashboard'),
    path('therapist-dashboard/', views.therapist_dashboard_view, name='therapist_dashboard'),
    path('status/<int:booking_id>/', views.update_booking_status_view, name='update_status'),
]
