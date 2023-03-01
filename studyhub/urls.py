from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('deck/', include('deck.urls.deck_urls')),
    path('card/', include('deck.urls.card_urls')),
    path('folder/', include('deck.urls.folder_urls')),
    path('courses/', include('deck.urls.course_urls')),
    path('user/', include('user_action.urls')),
    path('analytic/', include('analytic.urls')),
    path('api/health_check/', include('health_check.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
