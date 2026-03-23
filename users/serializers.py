from rest_framework import serializers
from users.models import User, Notification

class SimpleCustomUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'actor', 'receiver_user', 'message', 'link', 'is_read', 'created_at', 'updated_at']