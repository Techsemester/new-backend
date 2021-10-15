from rest_framework import serializers

from questions.models import Question, Answer, Vote, TagsQuestions

from users.models import User
from users.api.serializers import CountrySerializers, StateOnlyRetrieveSerializers


class TagQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TagsQuestions
        fields = ('id', 'title', 'slug', 'approval')


class QuestionSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField(method_name='get_user_details')
    total_answers = serializers.SerializerMethodField(method_name='count_answers')
    all_answers = serializers.SerializerMethodField(method_name='retrieve_all_answers')

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagsQuestions.objects.all()
    )

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Question
        fields = ['id', 'user', 'create_date', 'body', 'update_date', 'active', 'total_answers', 'title',
                  'slug', 'body', 'url', 'imageUrl', 'audio_url', 'video_url', 'youtube_url', 'all_answers', 'tags']
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


class AnswerSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField(method_name='total_upvotes')
    downvotes = serializers.SerializerMethodField(method_name='total_downvotes')
    in_reply_to_details = serializers.SerializerMethodField(method_name='reply_to_body')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'create_date', 'body', 'update_date', 'active', 'upvotes', 'downvotes',
                  'in_reply_to_details', 'slug', 'url', 'imageUrl', 'audio_url', 'video_url', 'youtube_url']

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
    state = serializers.SerializerMethodField('get_state_details')
    country = serializers.SerializerMethodField('get_country_details')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'image', 'email', 'gender', 'country', 'state')

    def get_country_details(self, obj):
        country = CountrySerializers(obj.country)
        return country.data

    def get_state_details(self, obj):
        serializer = StateOnlyRetrieveSerializers(obj.state)
        return serializer.data


class QuestionsUsersSerializers(QuestionSerializer):
    user = UserProfileDetailSerializers(read_only=True)
    tags = TagQuestionSerializer(read_only=True, many=True)