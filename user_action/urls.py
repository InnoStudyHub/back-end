from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user_action.views import FavouritesView, UserDeckView

urlpatterns = [
    path('favourite/add/', FavouritesView.as_view({"post": "add_favourite"}), name='favourite_add'),
    path('favourite/remove/', FavouritesView.as_view({"post": "remove_favourite"}), name='favourite_remove'),
    path('favourite/get/', FavouritesView.as_view({"get": "get_favourites"}), name='favourite_get'),
    path('decks/get/', UserDeckView.as_view({"get": "get_user_decks"}), name='get_my_decks'),
]