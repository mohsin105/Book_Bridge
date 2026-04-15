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
    profile_image = serializers.ImageField(required=False, allow_null=True)
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','email', 'first_name', 'last_name','bio', 'address', 'phone_number', 'profile_image', 'rating', 'late_return' ]
        read_only_fields = ['email', 'rating','late_return']

class NotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.SerializerMethodField(method_name='get_notification_type_display')
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'notification_type_display' ,'actor', 'receiver_user', 'message', 'link', 'is_read', 'created_at', 'updated_at']
    
    def get_notification_type_display(self, obj):
        return obj.get_notification_type_display()