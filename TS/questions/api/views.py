import json
import csv
# import pandas as pd
from django.conf import settings


from users.notifications import sendEmail
from django.utils import timezone
from questions.models import Answer, Question, Vote
from rest_framework import status, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from users.old_api.views import CustomPagination
from questions.models import *
from questions.api.serializers import *

@api_view(['GET',])
def country_state(request):
    """
    Get all active questions on the system
    Deliver result 20 items per page.
    """

    file = open(settings.COUNTRY_STACK, "r")
    industry_post = json.load(file)

    arrayArrs = []
    count = 0

    for n in industry_post:
        count = count + 1
        change = f"{n['regions']}"
        change = change.replace("'", "'")
        post = {
            "title": n['countryName'],
            "code": n['countryShortCode'],
            "dial": n['dialCode'],
            "flag": n['flag'],
            "regions": json.dumps(n.get('regions')),
        }
        fields = {
            "pk": count,
            "model": "users.countries",
            "fields": post
        }

        arrayArrs.append(fields)

    return Response(arrayArrs, status=status.HTTP_200_OK)

@api_view(['GET',])
def tags(request):
    """
    Get all active questions on the system
    Deliver result 20 items per page.
    """
    file = open(settings.TAGS_QUESTIONS, "r")
    industry_post = json.load(file)

    arrayArrs = []
    count = 0

    for n in industry_post:
        count = count + 1
        post = {
            "title": n,
            "approval": True
        }
        fields = {
            "pk": count,
            "model": "questions.tagsquestions",
            "fields": post
        }

        arrayArrs.append(fields)

    return Response(arrayArrs, status=status.HTTP_200_OK)


class QuestionUsersViewSets(generics.ListCreateAPIView):
    """
        user fetch uses
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Question.objects.all().order_by('-create_date')
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
            get all users questions
        """
        queryset = self.queryset.filter(user=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        """
            post questions
        """
        serializer.save(user = self.request.user)


class AnswersQuestionUsersViewSets(generics.ListCreateAPIView):
    """
        user fetch uses
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Answer.objects.all().order_by('-create_date')
    serializer_class = AnswerSerializer

    def get_queryset(self):
        """
            get all users questions
        """

        queryset = self.queryset.filter(user=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        """
            post questions
        """
        serializer.save()


class QuestionsRandomFromDifferentUsers(generics.ListAPIView):
    """
        This class is intended to fetch random question from users
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Question.objects.all().order_by('?')
    serializer_class = QuestionsUsersSerializers


class UpdateQuestionsViewSets(generics.RetrieveUpdateAPIView):
    """
        retrieve questions and update it's roles
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionsUsersSerializers
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Question.objects.filter(slug=self.kwargs['slug'])
        return queryset

    def perform_update(self, serializer):
        if serializer.is_valid():
            save = serializer.save()
            return save


class FileList(views.APIView):

    def get(self, request, format=None):
        file = open(settings.TAGS_QUESTION_STACK)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row[0])
        return Response(rows, status=status.HTTP_200_OK)


# class FileListPandas(views.APIView):
#
#     def get(self, request, format=None):
#         file = open(settings.TAGS_QUESTION_STACK)
#         rows = []
#         csvreader = pd.read_csv(file)
#         nicky = csvreader.to_json(orient = 'index')
#         return Response(nicky, status=status.HTTP_200_OK)