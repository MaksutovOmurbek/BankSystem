from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from apps.users.views import UserAPIVIewsSet, HistoryTransferAPIVIewsSet

router = DefaultRouter()
router.register('users', UserAPIVIewsSet, basename='api_user')
router.register('history_transfer', HistoryTransferAPIVIewsSet, basename='api_history_transfer')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh')
]

urlpatterns += router.urls
