from django.urls import path

from analytic.views import UserPropertiesViewSet

urlpatterns = [
    path('app/launch/', UserPropertiesViewSet.as_view({"post": "app_launch"}), name='app_launch'),
]
