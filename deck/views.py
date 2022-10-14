from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer


class DeckCreate(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    #def post(self):

