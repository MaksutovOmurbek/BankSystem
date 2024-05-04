from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.models import User, HistoryTransfer
from apps.users.serializers import UserSerializer, HistoryTransferSerializer
from apps.users.permissions import UserPermissions

class UserAPIVIewsSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return UserSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return (UserPermissions(),)
        return (AllowAny(),)
    
    def perform_update(self, serializer):
        return serializer.save(user = self.request.user)
    
class HistoryTransferAPIVIewsSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = HistoryTransfer.objects.all()
    serializer_class = HistoryTransferSerializer()
    



    
