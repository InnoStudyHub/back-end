from django.urls import path

from analytic.views import EventsViewSet

urlpatterns = [
    path('app/launch/', EventsViewSet.as_view({"post": "app_launch"}), name='app_launch'),
    path('app/onBackground/', EventsViewSet.as_view({"post": "app_on_background"}), name='app_on_background'),
    path('app/closed/', EventsViewSet.as_view({"post": "app_closed"}), name='app_closed'),
]
