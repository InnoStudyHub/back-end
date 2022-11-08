from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import DeckViewSet, FolderViewSet

urlpatterns = [
    path('create/', DeckViewSet.as_view({"post": "create"}), name='deck_create'),
    path('folder/create/', FolderViewSet.as_view({"post": "create"}), name='folder_create'),
    path('list/', DeckViewSet.as_view({"post": "list"}), name='deck_list'),
    path('getById/', DeckViewSet.as_view({"post": "get_by_id"}), name='get_by_id'),
    path('getByName/', DeckViewSet.as_view({"post": "get_by_name"}), name='get_by_name'),
    path('folder/list/', FolderViewSet.as_view({"get": "list"}), name='get_by_name')
]