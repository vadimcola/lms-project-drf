from rest_framework import serializers

from learn.serializers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(source='customer', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user



