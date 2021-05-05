from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from freight_terminal import util_views, settings

schema_view = get_schema_view(
   openapi.Info(
      title="Freight Terminal API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', include('companies.urls')),
    path('freights/', include('freights.urls')),
    path('devices/', include('devices.urls')),
    path('users/', include('users.urls')),

    # Utils
    path('backup/', util_views.BackupdDBAPIView.as_view(), name='backup'),
    path('restore/', util_views.RestoreDBAPIView.as_view(), name='restore'),

    # Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL)
