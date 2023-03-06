import json

from datetime import datetime
import jwt

import requests

from analytic.helpers import add_event
from analytic.models import EventsCategoryModel
from deck.models import Courses, Folder, UserFolderPermission
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
    user.set_password(register_data['password'])
    user.save()
    tokens = MyTokenObtainPairSerializer(register_data).validate(register_data)
    setup_courses(user)
    add_event(user, EventsCategoryModel.objects.get(event_category_name='Login from iu account'))
    return tokens


def get_moodle_user(user_email):
    request_url = f'https://{settings.MOODLE_API["URL"]}'
    request_params = {'moodlewsrestformat': 'json',
                      'wsfunction': 'core_user_get_users',
                      'wstoken': settings.MOODLE_API["TOKEN"],
                      'criteria[0][key]': 'email',
                      'criteria[0][value]': user_email}
    response = requests.post(url=request_url, params=request_params, verify=False)
    response_data = json.loads(response.content)

    if len(response_data['users']) != 0:
        return response_data['users'][0]
    return None


def setup_courses(user: User):
    moodle_user = get_moodle_user(user.email)
    year = 0

    if not moodle_user:
        year = 1
    else:
        first_access = moodle_user['firstaccess']
        first_dt_access = datetime.fromtimestamp(first_access)
        if first_dt_access.year == 2019:
            year = 4
        elif first_dt_access.year == 2020:
            year = 3
        elif first_dt_access.year == 2021:
            year = 2

    user.study_year = year
    user.save()
    courses = Courses.objects.filter(year=year)
    for course in courses:
        folder = Folder.objects.get_or_create(folder_name=course.course_name)

        if not UserFolderPermission.objects.filter(user=user, folder=folder[0], access_type=2).exists():
            user_folder_permission = UserFolderPermission.objects.create(user=user, folder=folder[0], access_type=2)
            user_folder_permission.save()
