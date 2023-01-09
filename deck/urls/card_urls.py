from django.urls import path
from deck.views import CardViewSet

urlpatterns = [
    path('delete/', CardViewSet.as_view({"put": "delete_cards"}), name='delete_cards'),
]
