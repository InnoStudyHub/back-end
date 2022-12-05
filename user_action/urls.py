from django.urls import path
from user_action.views import FavouritesView, UserDeckView, SearchView, UserLogsView, UserInfoAPIView

urlpatterns = [
    path('favourite/add/', FavouritesView.as_view({"post": "add_favourite"}), name='favourite_add'),
    path('favourite/remove/', FavouritesView.as_view({"post": "remove_favourite"}), name='favourite_remove'),
    path('favourite/get/', FavouritesView.as_view({"get": "get_favourites"}), name='favourite_get'),
    path('decks/get/', UserDeckView.as_view({"get": "get_user_decks"}), name='get_user_decks'),
    path('recent/', UserDeckView.as_view({"get": "get_recent_decks"}), name='get_recent_decks'),
    path('forYou/', UserDeckView.as_view({"get": "get_for_you_decks"}), name='get_for_you_decks'),
    path('search/', SearchView.as_view(), name='search_folder_and_deck'),
    path('info/', UserInfoAPIView.as_view(), name='get_user_by_id'),
    path('log/deck/', UserLogsView.as_view({"post": "deck_opened"}), name='user_logs_deck_opened'),
]