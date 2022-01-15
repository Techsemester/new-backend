from django.urls import path

app_name = 'questions'

from questions.api.views import *

urlpatterns = [
    path('tags', tags, name="tags"),
    path('country', country_state, name="country"),
    path('', QuestionUsersViewSets.as_view(), name='questioner'),
    path('answers', AnswersQuestionUsersViewSets.as_view(), name='answers'),
    path('answers/<slug:slug>', UpdateRepliesAnswersViewSets.as_view(), name='answer_replies'),
    path('json_file', FileList.as_view(), name='json_file'),
    path('blogs', BlogsPostsQuestionsViewSets.as_view(), name='blogs'),
    path('blogs/adminer', BlogsPostsQuestionsAdminViewSets.as_view(), name='blogs-adminer'),
    path('random', QuestionsRandomFromDifferentUsers.as_view(), name='random'),
    path('search/tags', SearchQuestionsTagsTitleSlug.as_view(), name='search'),
    path('<slug:slug>', UpdateQuestionsViewSets.as_view(), name='update'),
    path('blogs/<slug:slug>', RetrievePostsViewSets.as_view(), name='retrieve'),
    path('blogs/adminer/<slug:slug>', UpdateBlogPostsAdminerQuestionsViewSets.as_view(), name='retrieve_update'),
]