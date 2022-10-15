from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import DeckCreateView, FolderCreateView

urlpatterns = [
    path('create/', DeckCreateView.as_view(), name='deck_create'),
    path('folder/create/', FolderCreateView.as_view(), name='folder_create')
]