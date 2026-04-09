from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from users.models import Notification
from users.serializers import NotificationSerializer
from rest_framework.views import APIView
from borrow.models import BorrowRequest, BorrowRecord
from django.db.models import Q,Count
# Create your views here.
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(receiver_user = self.request.user)

class UserDashboard(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        requests = BorrowRequest.objects.aggregate(
            pending_sent = Count('id', filter=Q(status='PENDING', requested_by=user)),
            pending_received = Count('id', filter=Q(status='PENDING',book_copy__owner = user)),
            sent = Count('id', filter = Q(requested_by=user)),
        )
        records = BorrowRecord.objects.aggregate(
            active_borrowed = Count('id', filter=(Q(transaction_status='ACTIVE', borrower= user))),
            active_lent = Count('id', filter=Q(transaction_status='ACTIVE',owner = user)),
            overdue_borrowed = Count('id', filter=Q(transaction_status='OVERDUE', borrower= user)),
            overdue_lent = Count('id', filter=Q(transaction_status='OVERDUE',owner = user))
        )
        context={
            'requests':requests,
            'records':records
        }
        # print(context)
        return Response(context)
