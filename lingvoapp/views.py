import random
from datetime import date, timedelta
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from .models import Material,Dictionary,DictionaryInverted,AnswerOptions,Question
from .serializers import MaterialSerializer, MaterialSerializerList,DictionarySerializer,DictionaryInvertedSerializer,AnswerOptionsSerializer,RandomQuestionSerializer
from rest_framework.decorators import api_view
from googletrans import Translator
from rest_framework.views import APIView

#база, если нет слов
wordList=['it','he','go','do','I','want','think','sleep','sit','she','see','read','name','meet','like','his','help','have','happy','friend','food','father','family','eat','drive','drink','come','book','bed']
translationList=['оно','он','идти','делать','я','хотеть','думать','спать','сидеть','она','видеть','читать','имя','встречаться','нравиться','его','помощь','иметь','счастливый','друг','еда','отец','семья','еда','водить машину','пить','приходить','книга','кровать']


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


@api_view(['GET','DELETE'])
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


@api_view(['DELETE','GET','PUT'])
def dict(request, pk):
    # find tutorial by pk (id)
    # find tutorial by pk (id)
    try:
        dict = Dictionary.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        dictionary_serializer = DictionarySerializer(dict)
        return JsonResponse(dictionary_serializer.data)
    elif request.method == 'PUT':
        dictionary_data = JSONParser().parse(request)
        dictionary_serializer = DictionarySerializer(dict, data=dictionary_data)
        if dictionary_serializer.is_valid():
            dictionary_serializer.save()
            return JsonResponse(dictionary_serializer.data)
        return JsonResponse(dictionary_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    dictInverted=DictionaryInverted.objects.get(pk=pk)
    if request.method == 'DELETE':
        dict.delete()
        dictInverted.delete()
        return JsonResponse({'message': 'word was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# перевод-слово: формирование теста
class TranslationWord(APIView):

    def get(self, request, format=None, **kwargs):
        dict0=Dictionary.objects.all()
        if (dict0.count()>=20):
            dict0= Dictionary.objects.filter(state=0)
            c=dict0.count()
            startdate = date.today()
            enddate1 = startdate - timedelta(days=3)
            enddate2= startdate - timedelta(days=5)
            dict1 = Dictionary.objects.filter(edited__lte=enddate1, state=1)
            c1 = dict1.count()
            dict2 = Dictionary.objects.filter(edited__lte=enddate2, state=2)
            c2 = dict2.count()
            if(c>=10):
                dict0=dict0.order_by('?')[:10]
            elif ((c+c1)>=10):
                a=10-c
                dict0= dict0 | dict1.order_by('?')[:a]
            elif ((c+c1+c2)>=10):
                a=10-c-c1
                dict0 = dict0 | dict1 | dict2.order_by('?')[:a]
            else:
                a=10-c
                dict0= dict0| Dictionary.objects.all().order_by('?')[:a]
        else:
            n= len(wordList)
            for i in range(n):
                Dictionary.objects.create(word=wordList[i],translation=translationList[i])
                DictionaryInverted.objects.create(word=wordList[i],translation=translationList[i])
        dict0 = Dictionary.objects.all().order_by('?')[:10]
        for d in dict0:
            question = Question(questionText=d.translation)
            question.save()

            r=random.randint(0,3)
            for i in range(4):
                if(r==i):
                    rightAnswer = AnswerOptions(question=question, answerText=d.word, wordId=d.pk, isCorrect=True)
                    rightAnswer.save()
                else:
                    d1= Dictionary.objects.all().order_by('?').first()
                    while(d1.id==d.id):
                        d1 = Dictionary.objects.all().order_by('?').first()
                    wrongAnswer = AnswerOptions(question=question, answerText=d1.word, wordId=d1.pk, isCorrect=False)
                    wrongAnswer.save()

        question = Question.objects.all()
        serializer = RandomQuestionSerializer(question, many=True)
        a=serializer.data
        Question.objects.all().delete()
        return Response(a)


# слово-перевод: формирование теста
class WordTranslation(APIView):

    def get(self, request, format=None, **kwargs):
        dict0=DictionaryInverted.objects.all()
        if (dict0.count()>=20):
            dict0= DictionaryInverted.objects.filter(state=0)
            c=dict0.count()
            startdate = date.today()
            enddate1 = startdate - timedelta(days=3)
            enddate2= startdate - timedelta(days=5)
            dict1 = DictionaryInverted.objects.filter(edited__lte=enddate1, state=1)
            c1 = dict1.count()
            dict2 = DictionaryInverted.objects.filter(edited__lte=enddate2, state=2)
            c2 = dict2.count()
            if(c>=10):
                dict0=dict0.order_by('?')[:10]
            elif ((c+c1)>=10):
                a=10-c
                dict0= dict0 | dict1.order_by('?')[:a]
            elif ((c+c1+c2)>=10):
                a=10-c-c1
                dict0 = dict0 | dict1 | dict2.order_by('?')[:a]
            else:
                a=10-c
                dict0= dict0| DictionaryInverted.objects.all().order_by('?')[:a]
        else:
            n= len(wordList)
            for i in range(n):
                Dictionary.objects.create(word=wordList[i],translation=translationList[i])
                DictionaryInverted.objects.create(word=wordList[i],translation=translationList[i])
        dict0 = DictionaryInverted.objects.all().order_by('?')[:10]
        for d in dict0:
            question = Question(questionText=d.word)
            question.save()
            r = random.randint(0, 3)
            for i in range(4):
                if (r == i):
                    rightAnswer = AnswerOptions(question=question, answerText=d.word, wordId=d.pk, isCorrect=True)
                    rightAnswer.save()
                else:
                    d1 = DictionaryInverted.objects.all().order_by('?').first()
                    while (d1.id == d.id):
                        d1 = DictionaryInverted.objects.all().order_by('?').first()
                    wrongAnswer = AnswerOptions(question=question, answerText=d1.word, wordId=d1.pk, isCorrect=False)
                    wrongAnswer.save()

        question = Question.objects.all()
        serializer = RandomQuestionSerializer(question, many=True)
        a=serializer.data
        Question.objects.all().delete()
        return Response(a)





@api_view(['GET'])
def search(request):
    if request.method == 'GET':
        q=request.GET.get('word')
        print(q)
        vector = SearchVector('name')
        vector_trgm =  TrigramSimilarity('name',q)
        materials = Material.objects.annotate(search=vector).filter(search=q)
        materials2=Material.objects.annotate(similarity=vector_trgm).filter(similarity__gt=0.2)
        materials=materials|materials2
        print(materials)
    #    materials=Material.objects.filter(name__search=dat['word'])
        material_serializer = MaterialSerializerList(materials, many=True)
        return JsonResponse(material_serializer.data, safe=False)


@api_view(['POST'])
def change(request):
    if request.method == 'POST':
        words = JSONParser().parse(request)
        for word in words:
            pk=int(word)
            s=words.get(word)
            dict = Dictionary.objects.get(pk=pk)
            if (s=='0')|(s=='-1'):
                if (dict.state > 0):
                    dict.state -= 1
            elif (s=='1'):
                if (dict.state < 2):
                    dict.state += 1
            dict.save()
    return JsonResponse({'message': 'Words were updated successfully!'},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def change_inverted(request):
    if request.method == 'POST':
        words = JSONParser().parse(request)
        for word in words:
            pk=int(word)
            s=words.get(word)
            dict = DictionaryInverted.objects.get(pk=pk)
            if (s=='0')|(s=='-1'):
                if (dict.state > 0):
                    dict.state -= 1
            elif (s=='1'):
                if (dict.state < 2):
                    dict.state += 1
            dict.save()
    return JsonResponse({'message': 'Words were updated successfully!'},
                        status=status.HTTP_200_OK)




#git add -A
#git commit -m 'Update ALLOWED_HOSTS with site and development server URL'
#git push origin main
#git push heroku main
#heroku run python manage.py migrate




# изменение статуса слова DictionaryInverted

'''






@api_view(['GET'])
def dict_increment_inverted(request, pk):
    try:
        dict = DictionaryInverted.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if (dict.state<2):
            dict.state+=1
    dict.save()
    if request.method == 'GET':
        dictionary_serializer = DictionaryInvertedSerializer(dict)
        return JsonResponse(dictionary_serializer.data)


@api_view(['GET'])
def dict_decrement_inverted(request, pk):
    try:
        dict = DictionaryInverted.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if (dict.state > 0):
        dict.state -= 1
    dict.save()
    if request.method == 'GET':
        dictionary_serializer = DictionaryInvertedSerializer(dict)
        return JsonResponse(dictionary_serializer.data)
        
        @api_view(['GET'])
def dict_increment(request, pk):
    try:
        dict = Dictionary.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if (dict.state<2):
            dict.state+=1
    dict.save()
    if request.method == 'GET':
        dictionary_serializer = DictionarySerializer(dict)
        return JsonResponse(dictionary_serializer.data)


@api_view(['GET'])
def dict_decrement(request, pk):
    try:
        dict = Dictionary.objects.get(pk=pk)
    except Dictionary.DoesNotExist:
        return JsonResponse({'message': 'The word does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if (dict.state > 0):
        dict.state -= 1
    dict.save()
    if request.method == 'GET':
        dictionary_serializer = DictionarySerializer(dict)
        return JsonResponse(dictionary_serializer.data)

        '''
