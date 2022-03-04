from rest_framework import serializers
from django.contrib.auth import get_user_model
# from generic_relations.relations import GenericRelatedField

from .models import ObjectViewed, PivotObjectViewed
from users.api.serializers import UserSerializer

from questions.api.serializers import BlogPostsSerializer
from questions.models import BlogPost


class UserMetaSerializers(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'first_name', 'last_name', 'category', 'phone')


class ObjectViewSerializers(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = ObjectViewed
        fields = ('id', 'user', 'ip_address', 'content_type', 'viewed', 'actions', 'object_id',
                  'country_name', 'country_code', 'continent_code', 'continent_name', 'city',
                  'dma_code', 'latitude', 'longitude', 'postal_code', 'time_zone', 'timestamp',)
        read_only_fields = ('timestamp', 'id')


class AdminObjectViewSerializers(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = ObjectViewed
        fields = ('id', 'user', 'ip_address', 'content_type', 'viewed', 'actions', 'object_id',
                  'country_name', 'country_code', 'continent_code', 'continent_name', 'city',
                  'dma_code', 'latitude', 'longitude', 'postal_code', 'time_zone', 'timestamp',)
        read_only_fields = ('timestamp', 'id')


class AdminObjectivesViewedSerializers(serializers.ModelSerializer):

    class Meta:
        model = PivotObjectViewed
        fields = ('user', 'notification',)