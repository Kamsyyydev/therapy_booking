from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.models import User
from offers.models import Offer
from accounts.models import TherapistProfile
from .models import Booking
from .forms import BookingForm

@login_required
def book_offer_view(request, slug):
    offer = get_object_or_404(Offer, slug=slug, is_active=True)
    
    # Check student verification requirement
    is_verified_student = False
    if hasattr(request.user, 'student_verification'):
        is_verified_student = request.user.student_verification.is_verified
        
    if offer.is_student_offer and not is_verified_student:
        messages.warning(
            request,
            f'"{offer.name}" is reserved for verified students with a valid .edu or .edu.ng email. '
            'Please verify your academic email to unlock student discounts.'
        )
        return redirect(f'/accounts/verify-student/?next=/bookings/book/{offer.slug}/')

    selected_therapist_id = request.GET.get('therapist')
    initial_data = {}
    if selected_therapist_id:
        try:
            initial_data['therapist'] = User.objects.get(pk=selected_therapist_id)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.offer = offer
            
            # Combine chosen date and time slot
            date_val = form.cleaned_data.get('start_date')
            time_slot_str = form.cleaned_data.get('start_time_slot')
            
            if date_val and time_slot_str:
                hour, minute = map(int, time_slot_str.split(':'))
                naive_dt = datetime.combine(date_val, time(hour, minute))
                booking.start_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())
            elif offer.offer_type in [Offer.TYPE_SINGLE, Offer.TYPE_ASSESSMENT, Offer.TYPE_INTENSIVE, Offer.TYPE_GROUP]:
                # Default to tomorrow at 10:00 AM if no time provided for timed sessions
                tomorrow = timezone.now().date() + timezone.timedelta(days=1)
                naive_dt = datetime.combine(tomorrow, time(10, 0))
                booking.start_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())

            # Auto-assign a therapist if none chosen
            if not booking.therapist:
                first_therapist = User.objects.filter(therapist_profile__is_accepting_clients=True).first()
                if first_therapist:
                    booking.therapist = first_therapist

            # Generate meeting link / location
            if offer.slug == 'teletherapy' or 'video' in offer.description.lower():
                booking.meeting_link = f'https://meet.serenityhaven.ng/session-{request.user.id}-{int(timezone.now().timestamp())}'
            elif offer.slug == 'walk-talk-session':
                booking.meeting_link = 'Lekki Conservation Centre / Millennium Park Nature Trail, Nigeria'
            else:
                booking.meeting_link = 'Serenity Haven Wellness Suite, FUTO Road, Obinze, Owerri, Imo State, Nigeria (Phone/WhatsApp: 09166458597)'

            booking.status = Booking.STATUS_CONFIRMED
            booking.save()

            messages.success(
                request,
                f'Booking confirmed for "{offer.name}" with {booking.therapist.get_full_name() or booking.therapist.username}!'
            )
            return redirect('bookings:client_dashboard')
    else:
        form = BookingForm(initial=initial_data)

    therapists = TherapistProfile.objects.filter(is_accepting_clients=True).select_related('user')

    context = {
        'offer': offer,
        'form': form,
        'therapists': therapists,
        'is_verified_student': is_verified_student,
    }
    return render(request, 'bookings/book_session.html', context)

@login_required
def client_dashboard_view(request):
    if hasattr(request.user, 'therapist_profile'):
        return redirect('bookings:therapist_dashboard')

    all_bookings = Booking.objects.filter(client=request.user).select_related('offer', 'therapist', 'therapist__therapist_profile')
    
    now = timezone.now()
    upcoming_bookings = all_bookings.filter(
        status__in=[Booking.STATUS_CONFIRMED, Booking.STATUS_PENDING]
    ).filter(
        start_time__gte=now
    ).order_by('start_time')
    
    digital_bookings = all_bookings.filter(start_time__isnull=True, status=Booking.STATUS_CONFIRMED)
    
    past_bookings = all_bookings.exclude(
        id__in=upcoming_bookings.values_list('id', flat=True)
    ).exclude(
        id__in=digital_bookings.values_list('id', flat=True)
    ).order_by('-created_at')

    student_verification = getattr(request.user, 'student_verification', None)
    is_verified_student = student_verification.is_verified if student_verification else False

    context = {
        'upcoming_bookings': upcoming_bookings,
        'digital_bookings': digital_bookings,
        'past_bookings': past_bookings,
        'student_verification': student_verification,
        'is_verified_student': is_verified_student,
        'total_bookings': all_bookings.count(),
    }
    return render(request, 'bookings/client_dashboard.html', context)

@login_required
def therapist_dashboard_view(request):
    if not hasattr(request.user, 'therapist_profile'):
        messages.info(request, 'Therapist dashboard is only accessible to counselor accounts.')
        return redirect('bookings:client_dashboard')

    profile = request.user.therapist_profile
    therapist_bookings = Booking.objects.filter(therapist=request.user).select_related('client', 'offer').order_by('-start_time')
    
    now = timezone.now()
    upcoming_sessions = therapist_bookings.filter(
        status__in=[Booking.STATUS_CONFIRMED, Booking.STATUS_PENDING],
        start_time__gte=now
    ).order_by('start_time')
    
    past_sessions = therapist_bookings.filter(
        status__in=[Booking.STATUS_COMPLETED, Booking.STATUS_CANCELLED]
    ) | therapist_bookings.filter(start_time__lt=now)

    client_ids = therapist_bookings.values_list('client', flat=True).distinct()
    clients = User.objects.filter(id__in=client_ids)

    context = {
        'profile': profile,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions.order_by('-start_time')[:10],
        'total_sessions': therapist_bookings.count(),
        'clients_count': clients.count(),
    }
    return render(request, 'bookings/therapist_dashboard.html', context)

@login_required
def update_booking_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    is_authorized = (
        request.user == booking.therapist or
        request.user == booking.client or
        request.user.is_staff
    )
    
    if not is_authorized:
        messages.error(request, 'You do not have permission to modify this booking.')
        return redirect('bookings:client_dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f'Session status updated to "{booking.get_status_display()}".')

    if hasattr(request.user, 'therapist_profile'):
        return redirect('bookings:therapist_dashboard')
    return redirect('bookings:client_dashboard')
