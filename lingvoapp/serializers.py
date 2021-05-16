from rest_framework import serializers
from .models import Material,Dictionary,DictionaryInverted


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('id',
                  'name',
                  'created',
                  'text')

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