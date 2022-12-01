import jwt
import secrets

from rest_framework.exceptions import ValidationError

from studyhub import settings
from user.models import User
from user.serializers import RegistrationSerializer, MyTokenObtainPairSerializer


def register_iu_user(access_token, refresh_token):
    data = jwt.decode(jwt=access_token,
                      options={"verify_signature": False},
                      algorithms=['RS256'])

    register_data = {'email': data['email'],
                     'fullname': data['commonname'],
                     'password': settings.SECRET_KEY}

    if not User.objects.filter(email=data['email']):
        serializer = RegistrationSerializer(data=register_data)
        serializer.is_valid()
        serializer.save()

    user = User.objects.get(email=data['email'])
    user.iu_access_token = access_token
    user.iu_refresh_token = refresh_token
    user.save()

    tokens = MyTokenObtainPairSerializer(register_data).validate(register_data)

    return tokens
