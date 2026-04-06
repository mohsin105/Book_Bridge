from django.urls import path
from users.views import NotificationListView, UserDashboard

urlpatterns = [
    path('me/notifications/', NotificationListView.as_view(), name='notifications'),
    path('me/dashboard/', UserDashboard.as_view(), name='user-dashboard')
]
