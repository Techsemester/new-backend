import json
import csv
from django.conf import settings
from rest_framework import status, generics, views
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from questions.api.serializers import *
from analytics.signals import manageUsers


@api_view(['GET', ])
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


@api_view(['GET', ])
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


def get_return_methods(self, actions):

    queryset = self.queryset.filter(slug=self.kwargs['slug']).first()

    manageUsers({
        'user': queryset.user,
        'replies': self.request.user,
        'instance': queryset,
        'request': self.request,
        "actions": actions
    })

    return self.queryset


class SearchQuestionsTagsTitleSlug(generics.ListAPIView):
    queryset = TagsQuestions.objects.filter(approval=True)
    serializer_class = TagQuestionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering = ('-id',)
    search_fields = ['title']


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
        serializer.save(user=self.request.user)


class BlogsPostsQuestionsViewSets(generics.ListAPIView):
    """
        show all blogs post metros from all list for admirers only
    """
    queryset = BlogPost.objects.all().order_by('-create_date')
    serializer_class = BlogPostsSerializer


class BlogsPostsQuestionsAdminViewSets(generics.ListCreateAPIView):
    """
        show all blogs post metros from all list for admirers only
        add isAdminer here, admin only should be able to see this page
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = BlogPost.objects.all().order_by('-create_date')
    serializer_class = BlogPostsSerializer

    def perform_create(self, serializer):
        """
            post questions
        """
        serializer.save()


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
        store = serializer.save()

        question = Question.objects.filter(pk=self.request.data.get('question')).first()

        if store:
            manageUsers({
                'user': question.user,
                'replies': self.request.user,
                'instance': question,
                'request': self.request,
                "actions": f"{self.request.user.first_name} {self.request.user.last_name} replied to you posts"
            })


class QuestionsRandomFromDifferentUsers(generics.ListAPIView):
    """
        This class is intended to fetch random question from users
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Question.objects.all().order_by('?')
    serializer_class = QuestionsUsersSerializers


class UpdateQuestionsViewSets(generics.RetrieveUpdateDestroyAPIView):
    """
        retrieve questions and update it's roles
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    serializer_class = QuestionsUsersSerializers
    lookup_field = 'slug'

    def get_queryset(self):
        get_return_methods(self, f"{self.request.user.first_name} {self.request.user.last_name} viewed your posts")

    def perform_update(self, serializer):
        if serializer.is_valid():
            save = serializer.save()
            return save


class UpdateRepliesAnswersViewSets(generics.RetrieveUpdateDestroyAPIView):
    """
        retrieve questions and update it's roles
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.all()
    serializer_class = AnswerDetailsUsersSerializers
    lookup_field = 'slug'

    # def get_queryset(self):
    #     return self.queryset

    def perform_update(self, serializer):
        if serializer.is_valid():
            save = serializer.save()
            get_return_methods(self, f"{self.request.user.first_name} {self.request.user.last_name} replied to your post")
            return save


class UpdateBlogPostsAdminerQuestionsViewSets(generics.RetrieveUpdateAPIView):
    """
        retrieve questions and update it's roles,
        the admin will have update only
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BlogPost.objects.all().order_by('-create_date')
    serializer_class = BlogPostsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        get_return_methods(self, f"{self.request.user.first_name} {self.request.user.last_name} updated blog post")

    def perform_update(self, serializer):
        if serializer.is_valid():
            save = serializer.save()
            return save


class RetrievePostsViewSets(generics.RetrieveAPIView):
    """
        retrieve questions and update it's roles,
        the admin will have update only
    """
    queryset = BlogPost.objects.all().order_by('-create_date')
    serializer_class = BlogPostUsersTagsDetailSerializers
    lookup_field = 'slug'

    def get_queryset(self):
        get_return_methods(self,  f"{self.request.user.first_name} {self.request.user.last_name} viewed a blog post")


class FileList(views.APIView):

    def get(self, request, format=None):
        file = open(settings.TAGS_QUESTION_STACK)
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row[0])
        return Response(rows, status=status.HTTP_200_OK)


class VoteUpViewSetSerializer(views.APIView):
    """Get user update"""
    serializer_class = VoteSerializer

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
