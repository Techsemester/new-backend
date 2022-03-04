from rest_framework import serializers

from questions.models import Question, Answer, Vote, TagsQuestions, BlogPost

from users.models import User
from users.api.serializers import CountrySerializers, StateOnlyRetrieveSerializers


class TagQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagsQuestions
        fields = ('id', 'title', 'slug', 'approval')


class QuestionSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField(method_name='total_upvotes')
    downvotes = serializers.SerializerMethodField(method_name='total_downvotes')

    total_answers = serializers.SerializerMethodField(method_name='count_answers')
    all_answers = serializers.SerializerMethodField(method_name='retrieve_all_answers')

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagsQuestions.objects.all()
    )

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Question
        fields = ('id', 'user', 'code', 'create_date', 'body', 'update_date', 'active', 'total_answers', 'title',
                  'slug', 'body', 'url', 'imageUrl', 'audio_url', 'video_url', 'youtube_url', 'all_answers', 'tags',
                  'upvotes', 'downvotes')
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'create_date', 'update_date',)

    def count_answers(self, obj):
        votes = Answer.objects.filter(question=obj).count()
        return votes

    def retrieve_all_answers(self, obj):
        """
            All answers from each users
        """
        data = Answer.objects.filter(question=obj.id).values()
        return data

    def total_upvotes(self, obj):
        votes = Vote.objects.filter(question=obj.id, up=True).count()
        return votes

    def total_downvotes(self, obj):
        votes = Vote.objects.filter(question=obj.id, down=True).count()
        return votes


class BlogPostsSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagsQuestions.objects.all()
    )

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = BlogPost
        fields = ('id', 'user', 'code', 'create_date', 'body', 'update_date', 'active', 'title',
                  'slug', 'body', 'url', 'imageUrl', 'audio_url', 'video_url', 'youtube_url', 'tags')
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'create_date', 'update_date',)


class AnswerSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField(method_name='total_upvotes')
    downvotes = serializers.SerializerMethodField(method_name='total_downvotes')
    in_reply_to_details = serializers.SerializerMethodField(method_name='reply_to_body')

    class Meta:
        model = Answer
        fields = ('id', 'user', 'slug', 'question', 'create_date', 'body', 'update_date', 'active', 'upvotes', 'downvotes',
                  'in_reply_to_details', 'slug', 'url', 'imageUrl', 'audio_url', 'video_url', 'youtube_url')
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'create_date', 'update_date',)

    def reply_to_body(self, obj):
        """Give us the original answer body or return none if not applicable"""
        try: 
            return {
                "id": obj.in_reply_to.id,
                "user_id": obj.in_reply_to.user.id,
                "user": obj.in_reply_to.user.username,
                "body":obj.in_reply_to.body, 
                }
        except:
            return None

    
    def total_upvotes(self, obj):
        votes = Vote.objects.filter(answer=obj, up=True).count()
        return votes

    def total_downvotes(self, obj):
        votes = Vote.objects.filter(answer=obj, down=True).count()
        return votes


class UserProfileDetailSerializers(serializers.ModelSerializer):
    """
        few user details
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'image', 'email', 'gender', 'country', 'state')


class QuestionsUsersSerializers(QuestionSerializer):
    user = UserProfileDetailSerializers(read_only=True)
    tags = TagQuestionSerializer(read_only=True, many=True)


class AnswerDetailsUsersSerializers(AnswerSerializer):
    user = UserProfileDetailSerializers(read_only=True)


class BlogPostUsersTagsDetailSerializers(BlogPostsSerializer):
    user = UserProfileDetailSerializers(read_only=True)
    tags = TagQuestionSerializer(read_only=True, many=True)


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'user', 'question', 'answer', 'slug', 'up', 'down', 'create_date')
        lookup_field = 'slug'
        read_only_fields = ('id', 'slug', 'create_date', 'update_date', )

        # def create(self, validated_data):
        #     created = Vote.objects.get_or_create(
        #         answer=validated_data.get('user', None),
        #         question=validated_data.get('question', None),
        #         defaults={'user': validated_data.get('user', None)})
        #     return created
