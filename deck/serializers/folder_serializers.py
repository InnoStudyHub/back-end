from rest_framework import serializers

from deck.models import Folder


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['folder_name']

    def create(self, validated_data):
        return Folder.objects.create(**validated_data)