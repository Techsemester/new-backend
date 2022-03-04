from django.urls import path, include

from .views import *

app_name = "profiles"

urlpatterns = [
    path('followers', FollowersViewSet.as_view(), name='follower'),
    path('following', FollowingViewSet.as_view(), name='following'),
    path('unfollow/<int:pk>', UnFollowViewSet.as_view(), name='unfollow'),
    path('skills', SkillViewSet.as_view(), name='skill'),
    path('awards', AwardViewSet.as_view(), name='award'),
    path('projects', ProjectViewSet.as_view(), name='project'),
    path('experience', ExperienceViewSet.as_view(), name='experience'),
    path('education', EducationViewSet.as_view(), name='education'),
    path('certification', CertificationViewSet.as_view(), name='certification'),
    path('awards/<int:pk>', AwardsUpdateViewSet.as_view(), name='awards'),
    path('skills/<int:pk>', SkillsUpdateViewSet.as_view(), name='skills'),
    path('projects/<int:pk>', ProjectsUpdateViewSet.as_view(), name='projects'),
    path('education/<int:pk>', EducationViewSet.as_view(), name='educations'),
    path('experience/<int:pk>', ExperienceUpdateViewSet.as_view(), name='experiences'),
    path('certification/<int:pk>', CertificationsUpdateViewSet.as_view(), name='certification'),
]