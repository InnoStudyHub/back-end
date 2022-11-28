from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView

from studyhub.settings import logger
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from .serializers import RegistrationSerializer


class RegistrationAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: TokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Handle register user request: {request.data}")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = MyTokenObtainPairSerializer(request.data).validate(request.data)
            logger.info(f"User created: {user}")
            return Response(tokens, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    @extend_schema(
        request=MyTokenObtainPairSerializer,
        responses={201: TokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Handle login user request: {request.data}")
        return super().post(request, args, kwargs)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={
            (200, 'text/plain'): OpenApiResponse(description="Successfully logout")
        },
    )
    def post(self, request):
        user = request.user
        logger.info(f"Handle logout user request: {request.data}, from user: {user}")
        for token in OutstandingToken.objects.filter(user=user).exclude(
                id__in=BlacklistedToken.objects.filter(token__user=user).values_list('token_id', flat=True)):
            BlacklistedToken.objects.create(token=token)
        logger.info(f"User logged out: {user}")
        return Response("Successfully logout", status=status.HTTP_200_OK)


class UserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.request.user, content_type="application/json")
