from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Offer
from accounts.models import TherapistProfile

def home_view(request):
    category_filter = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()
    
    offers_qs = Offer.objects.filter(is_active=True)
    
    if category_filter and category_filter != 'all':
        offers_qs = offers_qs.filter(category=category_filter)
        
    if search_query:
        offers_qs = offers_qs.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(badge__icontains=search_query)
        )
    
    # Categorized dict for grouped display
    categories = [
        {'key': 'core', 'name': 'Core Sessions', 'desc': 'Foundational 1:1, assessment, and family counseling', 'icon': 'bi-heart-pulse'},
        {'key': 'packages', 'name': 'Packages & Bundles', 'desc': 'Multi-session plans with built-in cost savings', 'icon': 'bi-box-seam'},
        {'key': 'student', 'name': 'Student Offers', 'desc': 'Special discounted rates for verified .edu students', 'icon': 'bi-mortarboard'},
        {'key': 'mental_health', 'name': 'Mental Health & Wellness', 'desc': 'Specialized modalities: Somatic, Burnout, Walk & Talk', 'icon': 'bi-flower1'},
        {'key': 'memberships', 'name': 'Memberships', 'desc': 'Ongoing monthly support with guaranteed reserved slots', 'icon': 'bi-star'},
        {'key': 'addons', 'name': 'Add-Ons & Tools', 'desc': 'Supportive resources, digital workbooks, and check-ins', 'icon': 'bi-journal-check'},
    ]
    
    for cat in categories:
        cat['count'] = Offer.objects.filter(is_active=True, category=cat['key']).count()
        cat['offers'] = Offer.objects.filter(is_active=True, category=cat['key'])

    therapists = TherapistProfile.objects.filter(is_accepting_clients=True).select_related('user')[:4]
    
    context = {
        'offers': offers_qs,
        'categories': categories,
        'active_category': category_filter,
        'search_query': search_query,
        'total_offers': Offer.objects.filter(is_active=True).count(),
        'featured_therapists': therapists,
    }
    return render(request, 'home.html', context)

def offer_detail_view(request, slug):
    offer = get_object_or_404(Offer, slug=slug, is_active=True)
    therapists = TherapistProfile.objects.filter(is_accepting_clients=True).select_related('user')
    related_offers = Offer.objects.filter(category=offer.category, is_active=True).exclude(pk=offer.pk)[:3]
    
    context = {
        'offer': offer,
        'therapists': therapists,
        'related_offers': related_offers,
    }
    return render(request, 'offers/offer_detail.html', context)
