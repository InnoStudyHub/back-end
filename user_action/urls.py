from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user_action.views import FavouritesView

urlpatterns = [
    path('favourite/add/', FavouritesView.as_view({"post": "add_favourite"}), name='favourite_add'),
    path('favourite/remove/', FavouritesView.as_view({"post": "remove_favourite"}), name='favourite_remove')
]