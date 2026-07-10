from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Authentication & User Management
    path('users/', include('users.urls')),
    path('', include('users.urls')),      # Home page

    # Movie Module
    path('movies/', include('movies.urls')),

    # Reviews Module (Create this app if you separate reviews)
    path('reviews/', include('reviews.urls')),

    # Booking Module (Create this app if you separate bookings)
    path('bookings/', include('bookings.urls')),

    # Admin Dashboard (Optional)
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)