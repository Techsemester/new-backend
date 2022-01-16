from django.db.models import Q
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from analytics.models import ObjectViewed
from .serializer import ObjectViewSerializers, AdminObjectViewSerializers


class AnalysisInventionViewSet(generics.ListAPIView):
    queryset = ObjectViewed.objects.all().order_by('-timestamp')
    serializer_class = ObjectViewSerializers
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = ObjectViewed.objects.filter(user=self.request.user)
        return queryset


class AnalysisInventionUpdateViewSet(generics.UpdateAPIView):

    queryset = ObjectViewed.objects.all().order_by('-timestamp')
    serializer_class = ObjectViewSerializers

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]


class AnalysisInventionAdminViewSet(generics.ListAPIView):
    queryset = ObjectViewed.objects.filter(actions='created').order_by('-timestamp')
    serializer_class = ObjectViewSerializers

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser, ]


class AnalysisInventionAdminAllViewSet(generics.ListAPIView):
    queryset = ObjectViewed.objects.all().order_by('-timestamp')
    serializer_class = AdminObjectViewSerializers

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser, ]


class AdminInventorInvestorAnalysis(generics.ListAPIView):
    queryset = ObjectViewed.objects.all().order_by('-timestamp')
    serializer_class = AdminObjectViewSerializers

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.request is None:
            return ObjectViewed.objects.none()
        queryset = ObjectViewed.objects.filter(owner=self.kwargs['pk'])
        return queryset
