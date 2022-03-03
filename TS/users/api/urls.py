from django.urls import path, include, re_path

from .views import *

app_name = "users"

urlpatterns = [
    path('', ManageUserView.as_view(), name='user'),
    path('auth/', include('dj_rest_auth.urls'), name='login'),
    path('auth/facebook', FacebookViewSets.as_view(), name='fb_login'),
    path('countries', CountriesStateViewSets.as_view(), name='countries'),
    path('auth/google', GoogleSocialLoginViewSet.as_view(), name='gl_login'),
    path('auth/register/', include('dj_rest_auth.registration.urls'), name='register'),
]
