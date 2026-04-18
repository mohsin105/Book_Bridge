from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from users.models import Notification
from users.serializers import NotificationSerializer
from rest_framework.views import APIView
from borrow.models import BorrowRequest, BorrowRecord
from django.db.models import Q,Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(receiver_user = self.request.user).order_by('-created_at')

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


# class UserReviewViewSet(ModelViewSet):
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields= ['borrow_record', 'reviewed_user', 'reviewed_by']
#     permission_classes = [IsAdminOrAuthorOrReadOnly]

#     def get_queryset(self):
#         return UserReview.objects.all()
    
#     def get_serializer_class(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH']:
#             return UserReviewCreateSerializer
#         return UserReviewSerializer
    
#     def perform_create(self, serializer):
#         recordId = self.kwargs('record_pk')
#         # reviewed_user is the record owner
#         serializer.save(reviewed_by = self.request.user, reviewed_user=)
    
#     def perform_update(self, serializer):
#         return super().perform_update(serializer)
