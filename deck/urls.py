from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import DeckViewSet, FolderCreateView

urlpatterns = [
    path('create/', DeckViewSet.as_view({"post": "create"}), name='deck_create'),
    path('folder/create/', FolderCreateView.as_view(), name='folder_create'),
    path('list/', DeckViewSet.as_view({"post": "list"}), name='deck_list')
]