from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from offers.models import Offer
from accounts.models import TherapistProfile, StudentVerification

class Command(BaseCommand):
    help = 'Seeds all 25 therapy offers with images, reduced Nigerian Naira prices, Mrs. Angel & Mrs. Munalima, and demo accounts.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning database seeding...'))

        # 1. Clear existing offers
        Offer.objects.all().delete()

        # 2. Define all 25 offers with images and reduced Naira prices
        offers_data = [
            # CATEGORY 1: Core Sessions
            {
                'name': 'Single 1:1 Session',
                'category': Offer.CATEGORY_CORE,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 15000.00,
                'duration_minutes': 50,
                'sessions_included': 1,
                'badge': 'Popular',
                'image': 'offers/single_session.png',
                'tagline': 'Standard individual therapy for stress, personal growth, and clarity.',
                'description': 'A focused, confidential 50-minute individual therapy session designed to explore current challenges, develop coping strategies, and foster meaningful personal insight.',
                'features': 'Evidence-based CBT & ACT techniques\nPersonalized action plan\nFlexible in-person or online option\nCompassionate, non-judgmental space',
                'display_order': 1,
            },
            {
                'name': 'Extended Session',
                'category': Offer.CATEGORY_CORE,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 25000.00,
                'duration_minutes': 90,
                'badge': 'Deep Work',
                'image': 'offers/single_session.png',
                'tagline': 'For deeper exploratory work, trauma processing, and complex issues.',
                'description': 'A 90-minute extended session that gives you the time and emotional breathing room to work through complex trauma, grief, or major life shifts without feeling rushed.',
                'features': '90 uninterrupted minutes\nIdeal for EMDR, trauma, or deep breakthroughs\nDedicated grounding and integration time\nSummary notes and reflection prompts',
                'display_order': 2,
            },
            {
                'name': 'Couples/Family Session',
                'category': Offer.CATEGORY_CORE,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 20000.00,
                'duration_minutes': 60,
                'badge': 'Relationship',
                'image': 'offers/couples_therapy.jpg',
                'tagline': 'Strengthen communication, resolve recurring conflict, and rebuild trust.',
                'description': 'A 60-minute joint counseling session for couples or family members seeking to improve emotional connection, de-escalate conflicts, and develop constructive communication habits.',
                'features': 'Emotion-Focused Therapy (EFT) framework\nDe-escalation and active listening tools\nCollaborative relationship roadmap\nSafe, neutral mediation environment',
                'display_order': 3,
            },
            {
                'name': 'Initial Assessment',
                'category': Offer.CATEGORY_CORE,
                'offer_type': Offer.TYPE_ASSESSMENT,
                'price': 18000.00,
                'duration_minutes': 75,
                'badge': 'First Visit',
                'image': 'offers/single_session.png',
                'tagline': 'Comprehensive intake and customized mental wellness treatment plan.',
                'description': 'The recommended first step for new clients. A thorough 75-minute biopsychosocial assessment covering clinical history, current symptoms, goals, and customized therapeutic trajectory.',
                'features': 'Full diagnostic & symptom review\nTailored therapeutic goal setting\nTherapist match alignment\nIncludes clinical summary document',
                'display_order': 4,
            },
            {
                'name': 'Teletherapy Session',
                'category': Offer.CATEGORY_CORE,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 12000.00,
                'duration_minutes': 50,
                'badge': 'Online Video',
                'image': 'offers/single_session.png',
                'tagline': 'High-definition, secure video therapy from the comfort of your home or office.',
                'description': 'A 50-minute virtual session conducted over our encrypted telehealth platform. Receive the same warmth and efficacy of in-person therapy wherever you are in Nigeria or abroad.',
                'features': 'Secure encrypted video portal\nZero commute or traffic stress\nDigital intake & resource sharing\nAccessible on smartphone, laptop, or tablet',
                'display_order': 5,
            },

            # CATEGORY 2: Packages & Bundles
            {
                'name': '5-Session Starter Pack',
                'category': Offer.CATEGORY_PACKAGES,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 65000.00,
                'discounted_price': 75000.00,
                'duration_minutes': 50,
                'sessions_included': 5,
                'badge': 'Save ₦10,000',
                'image': 'offers/single_session.png',
                'tagline': 'Establish consistency with 5 sessions at a discounted bundle rate.',
                'description': 'Commit to meaningful progress with five 50-minute sessions. Perfect for tackling specific short-term challenges, establishing new coping habits, and building momentum.',
                'features': '5 full 50-minute sessions (₦13,000/session)\nFlexible scheduling over 3 months\nFree digital habit-tracking workbook\nPriority slot reservation',
                'display_order': 6,
            },
            {
                'name': '10-Session Growth Pack',
                'category': Offer.CATEGORY_PACKAGES,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 120000.00,
                'discounted_price': 150000.00,
                'duration_minutes': 50,
                'sessions_included': 10,
                'badge': 'Save 20%',
                'image': 'offers/single_session.png',
                'tagline': 'Our most popular package for sustainable healing and behavioral change.',
                'description': 'Ten 50-minute sessions providing sufficient runway to identify root patterns, resolve core emotional blocks, and achieve lasting transformation with 20% savings.',
                'features': '10 full 50-minute sessions (₦12,000/session)\nValid for up to 6 months\nIncludes Mid-Term Progress Review\nFree access to all digital workbooks',
                'display_order': 7,
            },
            {
                'name': '12-Session Transformation Pack',
                'category': Offer.CATEGORY_PACKAGES,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 140000.00,
                'discounted_price': 180000.00,
                'duration_minutes': 50,
                'sessions_included': 12,
                'badge': 'Save 25%',
                'image': 'offers/single_session.png',
                'tagline': 'Comprehensive long-term therapeutic journey with maximum savings.',
                'description': 'A robust 12-session transformation bundle designed for comprehensive healing, relationship restructuring, or chronic anxiety and mood management.',
                'features': '12 full 50-minute sessions (₦11,666/session)\nMaximum discount of 25%\nDirect counselor support between sessions\nValid for up to 12 months',
                'display_order': 8,
            },
            {
                'name': 'Assessment Package',
                'category': Offer.CATEGORY_PACKAGES,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 55000.00,
                'duration_minutes': 90,
                'sessions_included': 3,
                'badge': 'Comprehensive',
                'image': 'offers/single_session.png',
                'tagline': '3 extended diagnostic sessions + formal written psychological report.',
                'description': 'A formal clinical assessment package consisting of three 90-minute testing & clinical interviews, psychometric evaluations, and a formal clinical evaluation report.',
                'features': '3 x 90-minute clinical interviews\nStandardized psychometric testing\nFormal written psychological report\n1-hour feedback and recommendations session',
                'display_order': 9,
            },

            # CATEGORY 3: Student Offers
            {
                'name': 'Student Single Session',
                'category': Offer.CATEGORY_STUDENT,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 5000.00,
                'discounted_price': 15000.00,
                'duration_minutes': 50,
                'sessions_included': 1,
                'is_student_offer': True,
                'badge': 'Student Rate',
                'image': 'offers/student_counseling.jpg',
                'tagline': 'Affordable 1:1 mental health support for verified Nigerian students.',
                'description': 'A full 50-minute individual therapy session at an accessible student rate. Navigate academic pressure, project stress, career anxiety, or personal challenges.',
                'features': 'Requires active .edu or .edu.ng verification\nFull 50-minute clinical session\nAccessible student-friendly rate (₦5,000)\nIn-person (Obinze/Owerri) or online format',
                'display_order': 10,
            },
            {
                'name': 'Student 5-Pack',
                'category': Offer.CATEGORY_STUDENT,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 22000.00,
                'discounted_price': 25000.00,
                'duration_minutes': 50,
                'sessions_included': 5,
                'is_student_offer': True,
                'badge': 'Student Value',
                'image': 'offers/student_counseling.jpg',
                'tagline': 'Semester-long support package at only ₦4,400 per session.',
                'description': 'A 5-session student package designed to support you across an academic term. Ideal for midterms, finals, and ongoing emotional grounding.',
                'features': 'Requires active academic email verification\n5 sessions (₦4,400/session)\nFlexible scheduling around classes & practicals\nFree Anxiety & Stress digital guide',
                'display_order': 11,
            },
            {
                'name': '"Exam Crunch" Session',
                'category': Offer.CATEGORY_STUDENT,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 3000.00,
                'duration_minutes': 30,
                'sessions_included': 1,
                'is_student_offer': True,
                'badge': 'Quick Reset',
                'image': 'offers/student_counseling.jpg',
                'tagline': 'Rapid 30-minute stress-relief & grounding prior to exams & project defenses.',
                'description': 'A targeted, rapid 30-minute coaching and somatic reset session for students facing acute test anxiety, panic, or cognitive overload during exam periods.',
                'features': 'Requires active academic verification\n30-minute focused grounding\nImmediate somatic breathing exercises\nPanic de-escalation toolkit',
                'display_order': 12,
            },
            {
                'name': 'Student Group Session',
                'category': Offer.CATEGORY_STUDENT,
                'offer_type': Offer.TYPE_GROUP,
                'price': 1500.00,
                'duration_minutes': 60,
                'sessions_included': 1,
                'is_student_offer': True,
                'badge': 'Group Circle',
                'image': 'offers/student_counseling.jpg',
                'tagline': 'Peer-supported group therapy facilitated by a licensed counselor.',
                'description': 'A 60-minute therapist-moderated small group session (minimum 4 participants) exploring academic burnout, imposter syndrome, and social connection.',
                'features': 'Requires active academic email verification\n₦1,500 per student (min 4 participants)\nTherapist-led discussions & exercises\nBuild a supportive campus peer network',
                'display_order': 13,
            },

            # CATEGORY 4: Mental Health & Wellness
            {
                'name': 'Mental Health "Tune-Up"',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 18000.00,
                'duration_minutes': 75,
                'badge': 'Preventative',
                'image': 'offers/somatic_breathwork.jpg',
                'tagline': 'Preventative 75-minute check-in to realign habits and mindset.',
                'description': 'A proactive, preventative wellness session for individuals feeling generally stable who want to calibrate emotional resilience, optimize sleep & work boundaries, and prevent burnout.',
                'features': '75-minute holistic evaluation\nStress-load and boundary audit\nActionable 30-day wellness roadmap\nResource toolkit included',
                'display_order': 14,
            },
            {
                'name': 'Burnout Recovery Program',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_PACKAGE,
                'price': 95000.00,
                'duration_minutes': 50,
                'sessions_included': 8,
                'badge': '8-Week Program',
                'image': 'offers/somatic_breathwork.jpg',
                'tagline': 'Structured 8-week program: weekly sessions + mid-week check-ins.',
                'description': 'An intensive, structured 8-week intervention specifically curated for professionals, educators, and leaders suffering from chronic emotional exhaustion.',
                'features': '8 weekly 50-minute 1:1 sessions\nWeekly asynchronous check-ins\nNervous system regulation protocol\nComprehensive Burnout Recovery Workbook',
                'display_order': 15,
            },
            {
                'name': '"Walk & Talk" Session',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 12000.00,
                'duration_minutes': 50,
                'badge': 'Outdoor Nature',
                'image': 'offers/walk_and_talk.jpg',
                'tagline': 'Therapy in nature combining gentle movement with open dialogue.',
                'description': 'Step out of the traditional room into serene green spaces and botanical nature trails in Owerri. Combines gentle movement, fresh air, and cognitive processing to reduce stress levels.',
                'features': '50-minute outdoor nature session\nProven reduction in cortisol & blood pressure\nIdeal for clients who feel confined by sitting\nSerene walking trails',
                'display_order': 16,
            },
            {
                'name': 'Somatic/Body Session',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_SINGLE,
                'price': 15000.00,
                'duration_minutes': 50,
                'badge': 'Somatic Healing',
                'image': 'offers/somatic_breathwork.jpg',
                'tagline': 'Release stored physical stress through breathwork and somatic grounding.',
                'description': 'A 50-minute specialized session blending body-based psychotherapy, polyvagal nerve regulation, and guided breathwork to release trauma and physical tension stored in the body.',
                'features': 'Polyvagal somatic grounding\nGuided breathwork regulation\nNervous system down-regulation\nTake-home body scan audio guide',
                'display_order': 17,
            },
            {
                'name': 'Peer Support Group',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_GROUP,
                'price': 3500.00,
                'duration_minutes': 60,
                'sessions_included': 1,
                'badge': 'Community Circle',
                'image': 'offers/couples_therapy.jpg',
                'tagline': 'Weekly therapist-guided support group (minimum 6 participants).',
                'description': 'A welcoming, professionally facilitated circle where participants share mutual experiences, build empathy, and break feelings of isolation around anxiety, grief, or life transitions.',
                'features': '₦3,500 per person (min 6 people)\n60-minute moderated session\nShared wisdom and safe community\nWeekly structured topics',
                'display_order': 18,
            },
            {
                'name': 'Mental Health Day Intensive',
                'category': Offer.CATEGORY_MENTAL_HEALTH,
                'offer_type': Offer.TYPE_INTENSIVE,
                'price': 45000.00,
                'duration_minutes': 240,
                'badge': 'Half-Day Intensive',
                'image': 'offers/somatic_breathwork.jpg',
                'tagline': '4-hour deep dive immersion for rapid breakthroughs and reset.',
                'description': 'A transformative half-day (4-hour) intensive therapy retreat designed to bypass weeks of surface chatter, unpack deep-rooted blockages, and create a comprehensive life reboot.',
                'features': '4 hours of dedicated therapist focus\nIncludes somatic breaks & refreshments\nPersonalized transition manual\nFollow-up 30-min integration check-in',
                'display_order': 19,
            },

            # CATEGORY 5: Memberships
            {
                'name': 'Weekly Membership',
                'category': Offer.CATEGORY_MEMBERSHIPS,
                'offer_type': Offer.TYPE_MEMBERSHIP,
                'price': 50000.00,
                'duration_minutes': 50,
                'sessions_included': 4,
                'badge': 'Monthly Plan',
                'image': 'offers/single_session.png',
                'tagline': '4 sessions per month on convenient recurring monthly care.',
                'description': 'Our baseline recurring care membership. Includes four 50-minute sessions per month, automatic priority booking for your preferred day, and ongoing continuity of care.',
                'features': '4 sessions / month (₦12,500/session)\nAutomatic recurring billing\nPriority cancellation rescheduling\nAccess to all digital masterclasses',
                'display_order': 20,
            },
            {
                'name': 'Monthly Subscription',
                'category': Offer.CATEGORY_MEMBERSHIPS,
                'offer_type': Offer.TYPE_MEMBERSHIP,
                'price': 55000.00,
                'duration_minutes': 50,
                'sessions_included': 4,
                'badge': 'Reserved Prime Slot',
                'image': 'offers/single_session.png',
                'tagline': 'Weekly guaranteed reserved prime slot + direct messaging support.',
                'description': 'Never worry about therapist availability again. Secures a permanently reserved weekly prime time slot plus continuous portal messaging.',
                'features': 'Permanently reserved weekly slot\n4 sessions per month\nDirect asynchronous counselor messaging\nEmergency 24-hour rescheduling window',
                'display_order': 21,
            },
            {
                'name': 'Concierge Service',
                'category': Offer.CATEGORY_MEMBERSHIPS,
                'offer_type': Offer.TYPE_MEMBERSHIP,
                'price': 250000.00,
                'duration_minutes': 240,
                'sessions_included': 6,
                'badge': 'Executive VIP',
                'image': 'offers/single_session.png',
                'tagline': 'Executive tier: Priority 24/7 access + 6 half-day intensives.',
                'description': 'The ultimate bespoke mental health concierge for executives, founders, and public figures. Includes 6 custom intensives per month, priority scheduling, and direct line access.',
                'features': '6 half-day intensives per month\nGuaranteed same-day booking availability\nDirect encrypted clinician line\nCustomized private retreat option',
                'display_order': 22,
            },

            # CATEGORY 6: Add-Ons
            {
                'name': 'Mid-Week Check-in Call',
                'category': Offer.CATEGORY_ADDONS,
                'offer_type': Offer.TYPE_ADDON,
                'price': 3000.00,
                'duration_minutes': 15,
                'badge': 'Check-In',
                'image': 'offers/digital_journal.jpg',
                'tagline': '15-minute mid-week phone check-in for accountability and grounding.',
                'description': 'A quick 15-minute phone touchpoint between regular weekly sessions to review homework, maintain momentum, and tackle immediate hurdles.',
                'features': '15-minute focused phone call\nAccountability & goal checking\nQuick coping strategy refresher\nPairs with any active session',
                'display_order': 23,
            },
            {
                'name': 'Digital Workbook: Anxiety',
                'category': Offer.CATEGORY_ADDONS,
                'offer_type': Offer.TYPE_ADDON,
                'price': 2500.00,
                'duration_minutes': None,
                'badge': 'PDF Guide',
                'image': 'offers/digital_journal.jpg',
                'tagline': 'Interactive 60-page PDF clinical guide for overcoming panic & worry.',
                'description': 'An instant download interactive digital workbook packed with clinical CBT exercises, cognitive reframing worksheets, trigger tracking logs, and grounding scripts.',
                'features': 'Instant downloadable 60-page PDF\nFillable digital worksheets\nClinician-tested cognitive tools\nLifetime personal access',
                'display_order': 24,
            },
            {
                'name': 'Client Journal',
                'category': Offer.CATEGORY_ADDONS,
                'offer_type': Offer.TYPE_ADDON,
                'price': 1500.00,
                'duration_minutes': None,
                'badge': 'Digital Companion',
                'image': 'offers/digital_journal.jpg',
                'tagline': 'Guided digital therapy journal with daily reflection prompts.',
                'description': 'A structured digital journaling companion providing daily prompts, mood tracking graphs, session notes organization, and mindfulness reminders.',
                'features': '₦1,500/month recurring digital access\nDaily curated emotional check-ins\nExportable summaries for your therapist\nPrivate, encrypted cloud storage',
                'display_order': 25,
            },
        ]

        for item in offers_data:
            Offer.objects.create(**item)

        self.stdout.write(self.style.SUCCESS(f'Successfully created all {len(offers_data)} offers with images in Nigerian Naira (NGN)!'))

        # 3. Create Practitioners: Mrs. Angel & Mrs. Munalima
        TherapistProfile.objects.all().delete()
        User.objects.filter(username__in=['dr_sarah', 'marcus_vance', 'elena_rostova']).delete()

        therapists_data = [
            {
                'username': 'mrs_angel',
                'first_name': 'Angel',
                'last_name': 'Okafor, M.Sc.',
                'email': 'angel.okafor@serenityhaven.ng',
                'photo': 'therapists/mrs_angel.jpg',
                'title': 'Mrs. Angel — Licensed Clinical Psychologist & Mental Health Consultant',
                'specialization': 'Trauma, CBT, Anxiety Disorders, Personal Growth & Emotional Healing',
                'bio': 'Mrs. Angel is a seasoned clinical psychologist with over 10 years of practice in Nigeria. She provides a warm, faith-sensitive, evidence-based sanctuary for healing emotional pain and navigating life transitions.',
                'avatar_color': '#5B9EA7',
                'availability': {'monday': '09:00 - 17:00', 'wednesday': '09:00 - 17:00', 'friday': '09:00 - 16:00'},
            },
            {
                'username': 'mrs_munalima',
                'first_name': 'Munalima',
                'last_name': 'Bello, LMFT',
                'email': 'munalima.bello@serenityhaven.ng',
                'photo': None,
                'title': 'Mrs. Munalima — Family & Somatic Wellness Practitioner',
                'specialization': 'Couples & Family Counseling, Somatic Grounding, Burnout Recovery, Breathwork',
                'bio': 'Mrs. Munalima is a renowned marriage and family counselor specializing in relational restoration, nervous system regulation, and culturally grounded wellness strategies for busy Nigerian professionals and families.',
                'avatar_color': '#2C3E50',
                'availability': {'tuesday': '10:00 - 18:00', 'thursday': '10:00 - 18:00', 'saturday': '10:00 - 15:00'},
            },
        ]

        for t_info in therapists_data:
            user, created = User.objects.get_or_create(
                username=t_info['username'],
                defaults={
                    'first_name': t_info['first_name'],
                    'last_name': t_info['last_name'],
                    'email': t_info['email'],
                    'is_staff': True
                }
            )
            user.set_password('Therapy123!')
            user.first_name = t_info['first_name']
            user.last_name = t_info['last_name']
            user.email = t_info['email']
            user.save()
            
            TherapistProfile.objects.update_or_create(
                user=user,
                defaults={
                    'title': t_info['title'],
                    'specialization': t_info['specialization'],
                    'bio': t_info['bio'],
                    'photo': t_info.get('photo'),
                    'avatar_color': t_info['avatar_color'],
                    'availability': t_info['availability'],
                    'is_accepting_clients': True
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Created practitioners: Mrs. Angel (mrs_angel) and Mrs. Munalima (mrs_munalima)!'))

        # 4. Create Demo Nigerian Client & Student Accounts
        # Regular Client: Emeka Eze
        client_user, created = User.objects.get_or_create(
            username='emeka_client',
            defaults={
                'first_name': 'Emeka',
                'last_name': 'Eze',
                'email': 'emeka.eze@gmail.com',
            }
        )
        client_user.set_password('Client123!')
        client_user.first_name = 'Emeka'
        client_user.last_name = 'Eze'
        client_user.email = 'emeka.eze@gmail.com'
        client_user.save()

        # Verified Nigerian Student: Chioma Adebayo (FUTO Owerri)
        student_user, created = User.objects.get_or_create(
            username='chioma_student',
            defaults={
                'first_name': 'Chioma',
                'last_name': 'Adebayo',
                'email': 'chioma.adebayo@futo.edu.ng',
            }
        )
        student_user.set_password('Student123!')
        student_user.first_name = 'Chioma'
        student_user.last_name = 'Adebayo'
        student_user.email = 'chioma.adebayo@futo.edu.ng'
        student_user.save()
        
        StudentVerification.objects.update_or_create(
            user=student_user,
            defaults={
                'edu_email': 'chioma.adebayo@futo.edu.ng',
                'school_name': 'Federal University of Technology, Owerri (FUTO)',
                'is_verified': True,
                'verified_at': timezone.now()
            }
        )

        self.stdout.write(self.style.SUCCESS('Created demo client accounts: emeka_client / Client123! and chioma_student / Student123!'))
        self.stdout.write(self.style.SUCCESS('Database seeding complete! [OK]'))
