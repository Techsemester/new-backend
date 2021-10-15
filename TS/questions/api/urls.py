from django.urls import path

app_name = 'questions'

from questions.api.views import *

urlpatterns = [
    path('tags', tags, name="tags"),
    path('country', country_state, name="country"),
    path('', QuestionUsersViewSets.as_view(), name='questioner'),
    path('answers', AnswersQuestionUsersViewSets.as_view(), name='answers'),
    path('chioma', FileList.as_view(), name='chioma'),
    # path('panda', FileListPandas.as_view(), name='pandas'),
    path('random', QuestionsRandomFromDifferentUsers.as_view(), name='random'),
    path('<slug:slug>', UpdateQuestionsViewSets.as_view(), name='update'),
]