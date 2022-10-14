from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from user.models import User
from .forms import UploadFileForm
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from .serializers import RegistrationSerializer

from google.cloud import storage


class RegistrationAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: TokenObtainPairSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            tokens = MyTokenObtainPairSerializer(request.data).validate(request.data)
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
        return super().post(request, args, kwargs)


class UserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.request.user, content_type="application/json")

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)
    blob.make_public()

#@csrf_exempt
@api_view(['GET', 'POST'])
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(data=request.data, files=request.FILES)
        if form.is_valid():
            for x in form.files:
                upload_blob_from_memory('studyhub-data', form.data[x].read(), 'file/'+form.data[x].name)

    return HttpResponse('Upload successfully')