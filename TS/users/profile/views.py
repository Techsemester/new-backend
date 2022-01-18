from rest_framework import generics
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class FollowingViewSet(generics.ListCreateAPIView):
    """View following"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Follow.objects.all().order_by('-create_date')
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.data.get('follower'):
            if int(self.request.data.get('follower')) != self.request.user.id:
                serializer.save()


class FollowersViewSet(generics.ListAPIView):
    """View following"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Follow.objects.all().order_by('-create_date')
    serializer_class = FollowSerializer

    def get_queryset(self):
        return self.queryset.filter(follower=self.request.user)


class UnFollowViewSet(generics.UpdateAPIView):
    """View following"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Follow.objects.all().order_by('-create_date')
    serializer_class = FollowSerializer

    def perform_update(self, serializer):
        serializer.save(follow=False)


class ExperienceViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = ExperienceModels.objects.all().order_by('-created_at')
    serializer_class = ExperienceSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ExperienceUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = ExperienceModels.objects.all().order_by('-created_at')
    serializer_class = ExperienceSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SkillViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = SkillsModels.objects.all().order_by('-created_at')
    serializer_class = SkillsSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SkillsUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = SkillsModels.objects.all().order_by('-created_at')
    serializer_class = SkillsSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class CertificationViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = CertificationModels.objects.all().order_by('-created_at')
    serializer_class = CertificationSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CertificationsUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = CertificationModels.objects.all().order_by('-created_at')
    serializer_class = CertificationSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AwardViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = AwardsModels.objects.all().order_by('-created_at')
    serializer_class = AwardsSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AwardsUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = AwardsModels.objects.all().order_by('-created_at')
    serializer_class = AwardsSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProjectViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = ProjectsModels.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProjectsUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = ProjectsModels.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EducationViewSet(generics.ListCreateAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = EducationModels.objects.all().order_by('-created_at')
    serializer_class = EducationSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EducationsUpdateViewSet(generics.RetrieveUpdateDestroyAPIView):
    """Experience"""
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    queryset = EducationModels.objects.all().order_by('-created_at')
    serializer_class = EducationSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)