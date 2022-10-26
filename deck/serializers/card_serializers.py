from google.cloud import storage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from deck.models import Deck, Card

class CardCreateSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=1024, required=False, allow_blank=True, allow_null=True)
    question_image_key = serializers.CharField(max_length=1024, required=False, allow_blank=True, allow_null=True)
    answer_text = serializers.CharField(max_length=1024, required=False, allow_blank=True, allow_null=True)
    answer_image_keys = serializers.ListSerializer(child=serializers.CharField(), required=False, allow_empty=True)

    class Meta:
        fields = ['question_text', 'question_image_key', 'answer_text', 'answer_image_keys']

    def isImage(self, image):
        return (image.content_type is not None and image.content_type.split('/')[0] == 'image')

    def uploadPublicFileToStorage(self, bucket_name, contents, destination_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_string(contents)
        blob.make_public()
        return blob.public_url

    def uploadImage(self, validated_data, image_key):
        files = validated_data['files']
        deck_id = validated_data['deck_id']
        file = files.get(image_key)
        deck = Deck.objects.get(id=deck_id)
        folder_name = deck.folder.folder_name
        deck_name = deck.deck_name
        store_path = f'deck/{folder_name}/{deck_id}_{deck_name}/{image_key}_{file.name}'
        return self.uploadPublicFileToStorage('studyhub-data', file.read(), store_path)

    def getQuestionImageUrl(self, validated_data):
        if not validated_data.get('question_image_key'):
            return None

        question_image_key = validated_data['question_image_key']
        files = validated_data['files']
        if files.get(question_image_key):
            if not self.isImage(files[question_image_key]):
                raise ValidationError(f"{question_image_key} file is not image")
            return self.uploadImage(validated_data=validated_data, image_key=question_image_key)
        raise ValidationError(f"File with {question_image_key} key is not exist")

    def getAnswerImageUrls(self, validated_data):
        if not validated_data.get('answer_image_keys'):
            return None

        files = validated_data['files']
        answer_image_urls = []
        for answer_key in validated_data['answer_image_keys']:
            if files.get(answer_key):
                if not self.isImage(files[answer_key]):
                    raise ValidationError(f"{answer_key} file is not image")
            else:
                raise ValidationError(f"File with {answer_key} key is not exist")

        for answer_key in validated_data['answer_image_keys']:
            answer_image_urls.append(self.uploadImage(validated_data=validated_data, image_key=answer_key))
        return answer_image_urls

    def create(self, validated_data):
        deck_id = validated_data['deck_id']
        question_image_url = self.getQuestionImageUrl(validated_data=validated_data)
        answer_image_urls = self.getAnswerImageUrls(validated_data=validated_data)
        return Card.objects.create(deck_id=deck_id, question_text=validated_data['question_text'],
                                   answer_text=validated_data['answer_text'], question_image=question_image_url,
                                   answer_images=answer_image_urls)


class CardDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    question_image = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    answer_text = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    answer_images = serializers.JSONField(allow_null=True)

    class Meta:
        fields = ['id', 'question_text', 'question_image', 'answer_text', 'answer_images']
