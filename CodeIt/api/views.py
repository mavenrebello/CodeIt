from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from CodeIt.models import Question
from .serializers import QuestionSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/questions',
        'GET /api/questions/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getQuestions(request):
    questions=Question.objects.all()
    serializer=QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getQuestion(request, pk):
    question=Question.objects.get(id=pk)
    serializer=QuestionSerializer(question, many=False)
    return Response(serializer.data)