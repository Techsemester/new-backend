import sys
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import views, generics
from django.http import HttpResponseRedirect
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from users.models import Countries
from .serializers import CountryStateSerializers, UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""

        return self.request.user


class RegisterConfirmRedirect(views.APIView):
    def get(self, request, *args, **kwargs):
        """return to home page after email confirmation"""
        if (len(sys.argv) >= 2 and sys.argv[1] == 'runserver'):
            return HttpResponseRedirect(redirect_to='http://localhost:8080/login')
        else:
            return HttpResponseRedirect(redirect_to='https://inventorinvestorng.com/login')


class FacebookViewSets(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleSocialLoginViewSet(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class CountriesStateViewSets(generics.ListAPIView):

    """Show all countries"""
    queryset = Countries.objects.all()
    serializer_class = CountryStateSerializers


def EmailTemplates(request):
    """View function for home page of site."""
    return render(request, "email/communication.html")

