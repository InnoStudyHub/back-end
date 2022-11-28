from django.urls import path
from deck.views import DeckViewSet

urlpatterns = [
    path('create/', DeckViewSet.as_view({"post": "create"}), name='deck_create'),
    path('createFromSheet/', DeckViewSet.as_view({"post": "createFromGoogleSheet"}), name='deck_createFromSheet'),
    path('getById/', DeckViewSet.as_view({"post": "get_by_id"}), name='deck_get_by_id'),
    path('getByName/', DeckViewSet.as_view({"post": "get_by_name"}), name='deck_get_by_name')
]