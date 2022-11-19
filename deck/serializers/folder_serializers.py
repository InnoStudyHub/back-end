from rest_framework import serializers

from deck.models import Folder


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['folder_name']

    def create(self, validated_data):
        return Folder.objects.create(**validated_data)

class FolderDetailSerializer(serializers.Serializer):
    folder_name = serializers.CharField(max_length=255)
    folder_id = serializers.IntegerField()
    class Meta:
        fields = ['folder_name', 'folder_id']
