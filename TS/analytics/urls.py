from django.urls import path

from .views import *

app_name = 'analysis'

urlpatterns = [
    path('', AnalysisInventionViewSet.as_view(), name="inventor_analysis"),
    path('viewed/<int:pk>', AnalysisInventionUpdateViewSet.as_view(), name="inventor_viewed"),
    path('adminer', AnalysisInventionAdminViewSet.as_view(), name="inventor_analysis_admin"),
    path('activities', AnalysisInventionAdminAllViewSet.as_view(), name="inventor_activities_admin"),
    path('adminer/<int:pk>', AdminInventorInvestorAnalysis.as_view(), name="inventor_details_admin"),
]