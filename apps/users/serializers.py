from rest_framework import serializers
from django.utils.crypto import get_random_string


from apps.users.models import User, HistoryTransfer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'age', 'balance', 'wallet_address')
        
class HistoryTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryTransfer
        fields = ('id', 'from_user', 'to_user', 'is_completed', 'amount')