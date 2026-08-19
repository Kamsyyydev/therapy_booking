from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('offers.urls', namespace='offers')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
