from django.shortcuts import render
from rest_framework.generics import ListAPIView
from users.models import Notification
from users.serializers import NotificationSerializer
# Create your views here.
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(receiver_user = self.request.user)
