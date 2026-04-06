from rest_framework import serializers
from users.models import User, Notification
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email','first_name','last_name', 'phone_number', 'address', 'password']

class SimpleCustomUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email']

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id','email', 'first_name', 'last_name','bio', 'address', 'phone_number', 'profile_image', 'rating', 'late_return' ]
        read_only_fields = ['email', 'rating','late_return']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'actor', 'receiver_user', 'message', 'link', 'is_read', 'created_at', 'updated_at']