from rest_framework import serializers
from users.models import *


class FollowSerializer(serializers.ModelSerializer):
    """followed serializer"""
    class Meta:
        model = Follow
        fields = ('id', 'slug', 'user', 'create_date', 'update_date', 'follow', 'follower')
        read_only_fields = ('id', 'slug', 'create_date', 'update_date',)


class ExperienceSerializer(serializers.ModelSerializer):
    """followed serializer"""
    class Meta:
        model = ExperienceModels
        fields = ('id', 'user', 'created_at', 'experience',)
        read_only_fields = ('id', 'slug', 'create_date', 'update_date',)


class SkillsSerializer(serializers.ModelSerializer):
    """followed serializer"""
    class Meta:
        model = SkillsModels
        fields = ('id', 'user', 'created_at', 'skill',)
        read_only_fields = ('id', 'slug', 'created_at',)


class CertificationSerializer(serializers.ModelSerializer):
    """followed serializer"""
    class Meta:
        model = CertificationModels
        fields = ('id', 'user', 'created_at', 'name', 'image_url', )
        read_only_fields = ('id', 'slug', 'created_at',)


class AwardsSerializer(serializers.ModelSerializer):
    """followed serializer"""

    class Meta:
        model = AwardsModels
        fields = ('id', 'user', 'created_at', 'title', 'image_url', )
        read_only_fields = ('id', 'slug', 'created_at',)


class ProjectSerializer(serializers.ModelSerializer):
    """followed serializer"""

    class Meta:
        model = ProjectsModels
        fields = ('id', 'user', 'created_at', 'title', 'image_url', 'project_start_date', 'project_launch_date',
                  'description')
        read_only_fields = ('id', 'slug', 'created_at', )


class EducationSerializer(serializers.ModelSerializer):
    """followed serializer"""

    class Meta:
        model = EducationModels
        fields = ('id', 'user', 'created_at', 'image_url', 'experience', 'qualification', 'name_of_school',
                  'start_date', 'end_date')
        read_only_fields = ('id', 'slug', 'created_at', )