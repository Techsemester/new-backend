
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from users.api.views import RegisterConfirmRedirect

schema_view = get_schema_view(
   openapi.Info(
      title="Testing Api for all Users",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('oga/', admin.site.urls),
    path('', include('users.urls', namespace='default_user')),
    re_path('^', include('django.contrib.auth.urls')),
    path('api/users/', include('users.api.urls', namespace='users')),
    path('api/notifications/', include('analytics.urls', namespace='old_user')),
    path('api/question/', include('questions.api.urls')),
    path('rest/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/auth/accounts/', include('allauth.urls'), name='socialaccount_signup'),
    re_path(r'^api/auth/account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^api/auth/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/login/', RegisterConfirmRedirect.as_view(), name='redirect_after_confirm'),
    path('accounts/profile/', RegisterConfirmRedirect.as_view(), name='redirect_profile_confirm'),
]
