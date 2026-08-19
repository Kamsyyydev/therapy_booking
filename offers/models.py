from django.db import models
from django.utils.text import slugify

class Offer(models.Model):
    CATEGORY_CORE = 'core'
    CATEGORY_PACKAGES = 'packages'
    CATEGORY_STUDENT = 'student'
    CATEGORY_MENTAL_HEALTH = 'mental_health'
    CATEGORY_MEMBERSHIPS = 'memberships'
    CATEGORY_ADDONS = 'addons'

    CATEGORY_CHOICES = [
        (CATEGORY_CORE, 'Core Sessions'),
        (CATEGORY_PACKAGES, 'Packages & Bundles'),
        (CATEGORY_STUDENT, 'Student Offers'),
        (CATEGORY_MENTAL_HEALTH, 'Mental Health & Wellness'),
        (CATEGORY_MEMBERSHIPS, 'Memberships'),
        (CATEGORY_ADDONS, 'Add-Ons'),
    ]

    TYPE_SINGLE = 'single'
    TYPE_PACKAGE = 'package'
    TYPE_ASSESSMENT = 'assessment'
    TYPE_GROUP = 'group'
    TYPE_INTENSIVE = 'intensive'
    TYPE_MEMBERSHIP = 'membership'
    TYPE_ADDON = 'addon'

    OFFER_TYPE_CHOICES = [
        (TYPE_SINGLE, 'Single Session'),
        (TYPE_PACKAGE, 'Package / Bundle'),
        (TYPE_ASSESSMENT, 'Assessment'),
        (TYPE_GROUP, 'Group Session'),
        (TYPE_INTENSIVE, 'Day Intensive'),
        (TYPE_MEMBERSHIP, 'Membership'),
        (TYPE_ADDON, 'Add-On'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default=CATEGORY_CORE)
    offer_type = models.CharField(max_length=30, choices=OFFER_TYPE_CHOICES, default=TYPE_SINGLE)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Price in Nigerian Naira (₦)')
    discounted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Original before-discount price in ₦')
    is_student_offer = models.BooleanField(default=False)
    
    duration_minutes = models.IntegerField(null=True, blank=True, help_text='Duration in minutes (e.g. 50, 90, 240)')
    sessions_included = models.IntegerField(default=1, help_text='Number of sessions included in package')
    
    badge = models.CharField(max_length=50, blank=True, help_text='e.g. Student, Bestseller, New, Package, Save 20%')
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    features = models.TextField(blank=True, help_text='Line-separated list of key benefits')
    image = models.ImageField(upload_to='offers/', null=True, blank=True, help_text='Offer cover image or illustration')
    
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Offer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ₦{int(self.price):,}"

    def get_formatted_duration(self):
        if not self.duration_minutes:
            return 'Self-Paced / Digital'
        if self.duration_minutes >= 60:
            hours = self.duration_minutes // 60
            mins = self.duration_minutes % 60
            if mins == 0:
                return f"{hours} hr{'s' if hours > 1 else ''}"
            return f"{hours} hr {mins} mins"
        return f"{self.duration_minutes} mins"

    def get_display_price(self):
        val_str = f"₦{int(self.price):,}" if self.price == int(self.price) else f"₦{self.price:,.2f}"
        if self.category == self.CATEGORY_MEMBERSHIPS:
            return f"{val_str}/month"
        if self.offer_type == self.TYPE_GROUP:
            return f"{val_str}/person"
        return val_str

    def get_display_discounted_price(self):
        if not self.discounted_price:
            return None
        return f"₦{int(self.discounted_price):,}" if self.discounted_price == int(self.discounted_price) else f"₦{self.discounted_price:,.2f}"

    def get_features_list(self):
        if not self.features:
            return []
        return [line.strip() for line in self.features.split('\n') if line.strip()]
