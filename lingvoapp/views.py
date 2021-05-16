from django.shortcuts import render
# Create your views here.
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Material,Dictionary,DictionaryInverted
from .serializers import MaterialSerializer, MaterialSerializerList,DictionarySerializer,DictionaryInvertedSerializer
from rest_framework.decorators import api_view
from googletrans import Translator



@api_view(['GET', 'POST', 'DELETE'])
def material_list(request):
    if request.method == 'GET':
        materials = Material.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            materials = materials.filter(name__icontains=name)

        materials_serializer = MaterialSerializerList(materials, many=True)
        return JsonResponse(materials_serializer.data, safe=False)
    elif request.method == 'POST':
        material_data = JSONParser().parse(request)
        print(material_data)
        material_serializer = MaterialSerializer(data=material_data)
        if material_serializer.is_valid():
            material_serializer.save()
            return JsonResponse(material_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Material.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)
# GET list of tutorials, POST a new tutorial, DELETE all tutorials


@api_view(['GET', 'PUT', 'DELETE'])
def material_detail(request, pk):
    # find tutorial by pk (id)
    try:
        material = Material.objects.get(pk=pk)
    except Material.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        material_serializer = MaterialSerializer(material)
        return JsonResponse(material_serializer.data)
    elif request.method == 'PUT':
        material_data = JSONParser().parse(request)
        material_serializer = MaterialSerializer(material, data=material_data)
        if material_serializer.is_valid():
            material_serializer.save()
            return JsonResponse(material_serializer.data)
        return JsonResponse(material_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        material.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def dict_list(request):
    if request.method == 'GET':
        dicts = Dictionary.objects.all()

        dicts_serializer = DictionarySerializer(dicts, many=True)
        return JsonResponse(dicts_serializer.data, safe=False)
    elif request.method == 'DELETE':
        count = Dictionary.objects.all().delete()
        count=DictionaryInverted.objects.all().delete()

        return JsonResponse({'message': '{} Words were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def dict_one_word(request):
    if request.method == 'POST':
        dict_data = JSONParser().parse(request)
        word=dict_data["word"]
        translator = Translator()
        res = translator.translate(word, src='en', dest='ru')
        dict_data["translation"]=res.text
        dict_serializer = DictionarySerializer(data=dict_data)
        print(dict_serializer)
        if dict_serializer.is_valid():
           # material_serializer.save()
            return JsonResponse(dict_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(dict_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def dict_one_word_save(request):
    if request.method == 'POST':
        dict_data = JSONParser().parse(request)
        word=dict_data["word"]
        translator = Translator()
        res = translator.translate(word, src='en', dest='ru')
        dict_data["translation"]=res.text
        dict_serializer = DictionarySerializer(data=dict_data)
        dict_serializer2=DictionaryInvertedSerializer(data=dict_data)
        print(dict_serializer)


        if dict_serializer.is_valid():
            dict_serializer.save()
        if dict_serializer2.is_valid():
            dict_serializer2.save()
            return JsonResponse(dict_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(dict_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def dict_delete(request, pk):
    # find tutorial by pk (id)
    try:
        dict = Dictionary.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    dictInverted=DictionaryInverted.objects.get(pk=pk)
    if request.method == 'DELETE':
        dict.delete()
        dictInverted.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




