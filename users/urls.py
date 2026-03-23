from django.urls import path
from users.views import NotificationListView

urlpatterns = [
    path('me/notifications/', NotificationListView.as_view(), name='notifications')
]
