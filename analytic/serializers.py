import json

import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from analytic.helpers import get_user_analytic
from analytic.models import AppLaunchModel
from studyhub.settings import logger


class AppLaunchSerializer(serializers.Serializer):
    ip_address = serializers.CharField(max_length=256, required=True)
    platform = serializers.CharField(max_length=512, required=True)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        fields = ['ip_address', 'platform', 'user_id']

    def create(self, validated_data):
        ip_address = validated_data.get('ip_address')
        platform = validated_data.get('platform')
        user_id = validated_data.get('user_id', None)

        request_url = f'http://ip-api.com/json/{ip_address}?fields=status,country,regionName,city'
        response = requests.get(url=request_url, verify=False)

        if response.status_code != 200:
            logger.info(f'Response from geolocation api: {response.content}')
            raise ValidationError("Something goes wrong")

        data = json.loads(response.content)

        if data.get('status') == "fail":
            raise ValidationError("Not valid ip address")

        country = data.get('country')
        region_name = data.get('regionName')
        city = data.get('city')

        user_analytic = get_user_analytic(user_id)
        user_analytic.app_launches += 1
        user_analytic.save()

        return AppLaunchModel.objects.create(platform=platform, ip_address=ip_address,
                                             user_analytic=user_analytic, country=country,
                                             region_name=region_name, city=city)
