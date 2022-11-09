from django.urls import path
from deck.views import DeckViewSet

urlpatterns = [
    path('create/', DeckViewSet.as_view({"post": "create"}), name='deck_create'),
    path('search/', DeckViewSet.as_view({"post": "search"}), name='deck_list'),
    path('getById/', DeckViewSet.as_view({"post": "get_by_id"}), name='get_by_id'),
    path('getByName/', DeckViewSet.as_view({"post": "get_by_name"}), name='get_by_name')
]