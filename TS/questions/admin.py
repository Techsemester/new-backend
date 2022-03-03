from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from questions.models import Question, Answer, Vote

class QuestionAdmin(ImportExportModelAdmin):
	model = Question
	list_display = ['user', 'create_date', 'update_date', 'body', 'active']
admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(ImportExportModelAdmin):
	model = Answer
	list_display = ['user', 'question', 'create_date', 'body', 'update_date', 'active']
admin.site.register(Answer, AnswerAdmin)