from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from deck.helpers.card_helpers import isImage, getQuestionImageUrl, \
    getAnswerImageUrls, toImage
from deck.models import Card


class CardCreateSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=1024,
                                          required=False, allow_blank=True, allow_null=True, default="")
    question_image_key = serializers.CharField(max_length=1024,
                                               required=False, allow_blank=True, allow_null=True, default="")
    answer_text = serializers.CharField(max_length=1024,
                                        required=False, allow_blank=True, allow_null=True, default="")
    answer_image_keys = serializers.ListSerializer(child=serializers.CharField(),
                                                   required=False, allow_empty=True, default=[])

    class Meta:
        fields = ['question_text', 'question_image_key', 'answer_text', 'answer_image_keys']

    def create(self, validated_data):
        deck_id = validated_data['deck_id']
        files = validated_data['files']
        question_image_key = validated_data['question_image_key']
        answer_image_keys = validated_data['answer_image_keys']

        keys = list.copy(answer_image_keys)
        if question_image_key:
            keys.append(question_image_key)

        new_files = {}

        for key in keys:
            if not files.get(key):
                raise ValidationError(f"File with {key} key is not exist")

            new_files[key] = toImage(files[key], key)

            if not isImage(new_files[key]):
                raise ValidationError(f"{key} file is not image")

        question_image_url = getQuestionImageUrl(files=new_files,
                                                 deck_id=deck_id,
                                                 question_image_key=question_image_key)
        answer_image_urls = getAnswerImageUrls(files=new_files,
                                               deck_id=deck_id,
                                               answer_image_keys=answer_image_keys)
        return Card.objects.create(deck_id=deck_id, question_text=validated_data['question_text'],
                                   answer_text=validated_data['answer_text'], question_image=question_image_url,
                                   answer_images=answer_image_urls)


class CardDetailSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    question_text = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    question_image = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    answer_text = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    answer_images = serializers.ListSerializer(child=serializers.CharField(), allow_null=True)

    class Meta:
        fields = ['card_id', 'question_text', 'question_image', 'answer_text', 'answer_images']
