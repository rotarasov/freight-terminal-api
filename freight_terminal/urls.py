from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', include('companies.urls')),
    path('freights/', include('freights.urls')),
    path('devices/', include('devices.urls')),
    path('users/', include('users.urls'))
]
