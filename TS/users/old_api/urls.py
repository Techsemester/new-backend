from django.urls import path

from users.old_api.views import(
    RegisterApiView,
    UserUpdateApiView,
    verify_email,
    token_request,
    password_reset,
    ChangePassword,
    get_username,
    loginx,
    get_profile,
    contact_us,
    update_phone_email,
    profile_pic,
)

app_name = "accounts"


urlpatterns = [
        path('register/', RegisterApiView.as_view(), name="register"),
        path('login/', loginx, name="login"),
        path('change_password/', ChangePassword.as_view(), name="change_password"),
        path('get_username/', get_username, name="get_username"),
        path('verify_email/', verify_email, name="verify_email"),
        path('token_request/', token_request, name="token_request"),
        path('password_reset/', password_reset, name="password_reset"),
        path('profile-update/<int:pk>/', UserUpdateApiView.as_view(), name="update"),
        path('get_profile/', get_profile, name="get_profile"),
        path('contact_us/', contact_us, name="contact_us"),
        path('update_phone_email/', update_phone_email, name="update_phone_email"),
        path('profile_pic/', profile_pic, name="profile_pic"),
]
