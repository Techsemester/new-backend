from django.db import models
from users.models import User
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField

from techsemester.utils import unique_slug_generator, unique_slug_question_generator


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def slug_related_question(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_question_generator(instance)


class Question(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    title                   = models.CharField(max_length=255, blank=True, null=True)
    slug                   = models.CharField(max_length=255, blank=True, null=True)
    body                    = RichTextField(blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)
    imageUrl                = models.URLField(blank=True, null=True)
    audio_url               = models.URLField(blank=True, null=True)
    video_url               = models.URLField(blank=True, null=True)
    youtube_url             = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    total_answers           = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Answer(models.Model):
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    question                = models.ForeignKey(Question, on_delete=models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    update_date             = models.DateTimeField(auto_now=True)
    body                    = RichTextField(blank=True, null=True)
    slug                    = models.CharField(max_length=255, blank=True, null=True)
    url                     = models.URLField(blank=True, null=True)
    imageUrl                = models.URLField(blank=True, null=True)
    audio_url               = models.URLField(blank=True, null=True)
    video_url               = models.URLField(blank=True, null=True)
    youtube_url             = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    in_reply_to             = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    chosen                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class Vote(models.Model):
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    question              = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    answer                = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    slug                  = models.CharField(max_length=255, blank=True, null=True)
    create_date           = models.DateTimeField(auto_now_add=True)
    update_date           = models.DateTimeField(auto_now=True)
    up                    = models.BooleanField(default=False)
    down                  = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'


pre_save.connect(slug_generator, sender=Question)
pre_save.connect(slug_related_question, sender=Answer)
pre_save.connect(slug_related_question, sender=Vote)