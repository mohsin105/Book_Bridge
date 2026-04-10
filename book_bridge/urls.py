from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root_view 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Bookbridge API",
      default_version='v1',
      description="A Peer-to-Peer Book Sharing Platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mohsinibnaftab@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', api_root_view),
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('api/v1/', include('api.urls'), name='api-root'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
