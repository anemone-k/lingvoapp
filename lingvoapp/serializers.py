from rest_framework import serializers
from .models import Material,Dictionary,DictionaryInverted,Question, AnswerOptions


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('id',
                  'name',
                  'created',
                  'text',
                  'youtubeUrl')

class MaterialSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id',
                  'name',
                  'created')


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('id',
                  'word',
                  'translation',
                  'state',
                  'edited')


class DictionaryInvertedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryInverted
        fields = ('id',
                  'word',
                  'translation',
                  'state',
                  'edited')


class AnswerOptionsSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnswerOptions
        fields = [
            'answerText',
            'isCorrect',
            'wordId'
        ]

class RandomQuestionSerializer(serializers.ModelSerializer):

    answer = AnswerOptionsSerializer(many=True, read_only=True)

    class Meta:

        model = Question
        fields = [
            'questionText','answer'
        ]