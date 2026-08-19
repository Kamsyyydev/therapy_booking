from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from offers.models import Offer
from accounts.models import TherapistProfile, StudentVerification
from bookings.models import Booking

class TherapyBookingPlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create standard offer
        self.standard_offer = Offer.objects.create(
            name='Single 1:1 Session',
            category=Offer.CATEGORY_CORE,
            offer_type=Offer.TYPE_SINGLE,
            price=15000.00,
            duration_minutes=50,
            sessions_included=1,
            description='Standard therapy session in Owerri',
            is_active=True
        )
        
        # Create student offer
        self.student_offer = Offer.objects.create(
            name='Student Single Session',
            category=Offer.CATEGORY_STUDENT,
            offer_type=Offer.TYPE_SINGLE,
            price=5000.00,
            duration_minutes=50,
            sessions_included=1,
            is_student_offer=True,
            description='FUTO & Nigerian student discounted therapy',
            is_active=True
        )

        # Create Client user
        self.client_user = User.objects.create_user(
            username='emeka_client',
            email='emeka@gmail.com',
            password='TestPassword123'
        )

        # Create Nigerian Student user
        self.student_user = User.objects.create_user(
            username='chioma_student',
            email='chioma@futo.edu.ng',
            password='TestPassword123'
        )
        self.student_verif = StudentVerification.objects.create(
            user=self.student_user,
            edu_email='chioma@futo.edu.ng',
            school_name='Federal University of Technology, Owerri (FUTO)',
            is_verified=True
        )

        # Create Therapist: Mrs. Angel
        self.therapist_user = User.objects.create_user(
            username='mrs_angel',
            first_name='Angel',
            last_name='Okafor',
            email='angel.okafor@serenityhaven.ng',
            password='TestPassword123'
        )
        self.therapist_profile = TherapistProfile.objects.create(
            user=self.therapist_user,
            title='Mrs. Angel — Licensed Clinical Psychologist',
            specialization='Anxiety & CBT',
            availability={'monday': '9-5', 'tuesday': '9-5'}
        )

    def test_offers_catalog_view(self):
        """Test home catalog loads and contains offers in Naira"""
        response = self.client.get(reverse('offers:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Single 1:1 Session')
        self.assertContains(response, 'Student Single Session')
        self.assertContains(response, '₦15,000')

    def test_offers_category_filter(self):
        """Test filtering catalog by category"""
        response = self.client.get(reverse('offers:home') + '?category=student')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Single Session')

    def test_offer_detail_view(self):
        """Test offer detail page displays correctly with Naira currency"""
        response = self.client.get(reverse('offers:offer_detail', kwargs={'slug': self.standard_offer.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.standard_offer.name)
        self.assertContains(response, '₦15,000')

    def test_booking_standard_offer(self):
        """Test client booking a standard offer"""
        self.client.login(username='emeka_client', password='TestPassword123')
        
        response = self.client.post(
            reverse('bookings:book_offer', kwargs={'slug': self.standard_offer.slug}),
            {
                'therapist': self.therapist_user.id,
                'start_date': '2026-09-01',
                'start_time_slot': '10:00',
                'client_notes': 'Focus on stress management'
            }
        )
        self.assertEqual(response.status_code, 302)
        
        booking = Booking.objects.filter(client=self.client_user, offer=self.standard_offer).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.therapist, self.therapist_user)
        self.assertEqual(booking.status, Booking.STATUS_CONFIRMED)

    def test_student_offer_requires_verification(self):
        """Test unverified client is redirected when booking student offer"""
        self.client.login(username='emeka_client', password='TestPassword123')
        response = self.client.get(reverse('bookings:book_offer', kwargs={'slug': self.student_offer.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/verify-student/', response.url)

    def test_verified_student_can_book_student_offer(self):
        """Test verified student can access student booking directly"""
        self.client.login(username='chioma_student', password='TestPassword123')
        response = self.client.get(reverse('bookings:book_offer', kwargs={'slug': self.student_offer.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book: Student Single Session')

    def test_student_verification_auto_verify_nigerian_domain(self):
        """Test verify_if_eligible method correctly checks .edu.ng domain"""
        unverified_ng = StudentVerification(user=self.client_user, edu_email='test@futo.edu.ng')
        self.assertTrue(unverified_ng.verify_if_eligible())
        self.assertTrue(unverified_ng.is_verified)

        non_edu = StudentVerification(user=self.client_user, edu_email='test@yahoo.com')
        self.assertFalse(non_edu.verify_if_eligible())

    def test_therapist_dashboard_access(self):
        """Test therapist dashboard redirects non-therapists and allows Mrs. Angel"""
        self.client.login(username='emeka_client', password='TestPassword123')
        response = self.client.get(reverse('bookings:therapist_dashboard'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='mrs_angel', password='TestPassword123')
        response = self.client.get(reverse('bookings:therapist_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upcoming Clinical Schedule')
