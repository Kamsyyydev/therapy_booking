from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking
from accounts.models import TherapistProfile

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().strftime('%Y-%m-%d')
        }),
        required=False,
        label='Preferred Session Date',
        help_text='Choose any date from today onwards'
    )
    start_time_slot = forms.ChoiceField(
        choices=[
            ('09:00', '09:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('13:00', '01:00 PM'),
            ('14:00', '02:00 PM'),
            ('15:00', '03:00 PM'),
            ('16:00', '04:00 PM'),
            ('17:00', '05:00 PM'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Preferred Time Slot'
    )

    therapist = forms.ModelChoiceField(
        queryset=User.objects.filter(therapist_profile__is_accepting_clients=True),
        required=False,
        empty_label="Any Available Therapist (Auto-Match)",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Therapist / Specialist'
    )

    class Meta:
        model = Booking
        fields = ('therapist', 'client_notes')
        widgets = {
            'client_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share any specific topics or goals you would like to focus on during your session...'
            }),
        }
        labels = {
            'client_notes': 'Session Focus / Client Notes (Optional)'
        }
