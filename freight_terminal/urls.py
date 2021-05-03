from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from freight_terminal import util_views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', include('companies.urls')),
    path('freights/', include('freights.urls')),
    path('devices/', include('devices.urls')),
    path('users/', include('users.urls')),

    # Utils
    path('backup/', util_views.BackupdDBAPIView.as_view(), name='backup'),
    path('restore/', util_views.RestoreDBAPIView.as_view(), name='restore')
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
