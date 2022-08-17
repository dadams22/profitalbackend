from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    is_plaid_connected = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'is_plaid_connected')
        write_only_fields = ('password',)
        read_only_fields = ('is_plaid_connected',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    def get_is_plaid_connected(self, user) -> bool:
        return user.plaid_access_token is not None
