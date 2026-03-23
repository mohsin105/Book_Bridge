from django.shortcuts import render, get_object_or_404
from datetime import timedelta,datetime, timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from borrow.models import BorrowRequest, BorrowRecord,BorrowExtensionRequest
from borrow.serializers import BorrowRequestSerializer, BorrowRecordSerializer, RequestCreateSerializer, RequestPatchSerializer, ExtensionRequestSerialier, ExtensionCreateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import Notification
from books.models import BookCopy
from django.conf import settings
# Create your views here.

"""  BorrowRequest CRUD operations ---------->   """

class BorrowRequestListView(ListCreateAPIView):
    # queryset = BorrowRequest.objects.all()
    # serializer_class = BorrowRequestSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BorrowRequest.objects.all()
        
        return BorrowRequest.objects.filter(requested_by = self.request.user, status = 'PENDING')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RequestCreateSerializer
        return BorrowRequestSerializer
        
    def perform_create(self, serializer):
        requestObj = serializer.save(requested_by = self.request.user)
        bookCopyObj = serializer.validated_data.get('book_copy')
        owner = bookCopyObj.owner
        Notification.objects.create(
            notification_type = 'borrow_request',
            actor = self.request.user,
            receiver_user = owner,
            message = f'{self.request.user} has requested {bookCopyObj.book.title} from you',
            link = f'{settings.BACKEND_URL}/api/v1/borrow/user/pending-requests/{requestObj.id}/'
        )

class SpecificBorrowRequestView(RetrieveUpdateDestroyAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return BorrowRequest.objects.filter(requested_by = self.request.user, status = 'PENDING')
    
    def perform_update(self, serializer):
        if serializer.validated_data.get('status') != 'CANCELLED':
            return Response(status = status.HTTP_403_FORBIDDEN)
        serializer.save()

@api_view(['GET'])
def pending_requests(request):
    if request.method == 'GET':
        qs = BorrowRequest.objects.filter(book_copy__owner = request.user, status = 'PENDING' )
        serializer = BorrowRequestSerializer(qs,many = True)
        return Response(serializer.data)

@api_view(['GET', 'PATCH'])
def specific_pending_request(request, id):
    if request.method == 'GET':
        qs = BorrowRequest.objects.get(id = id, book_copy__owner = request.user, status = 'PENDING')
        serializer = BorrowRequestSerializer(qs)
        return Response(serializer.data)

class SpecificPendingRequest(RetrieveUpdateAPIView):
    # queryset = BorrowRequest.objects.filter(book_copy__owner = )
    http_method_names = ['get', 'patch', 'delete', 'head', 'options', 'trace']
    # serializer_class = BorrowRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return BorrowRequest.objects.filter(book_copy__owner = self.request.user, status = 'PENDING')
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RequestPatchSerializer
        return BorrowRequestSerializer
    
    def perform_update(self, serializer):
        obj = self.get_object()
        # print("perform update called")
        if serializer.validated_data.get('status')=='ACCEPTED':
            recordObj = BorrowRecord.objects.create(
                borrower = obj.requested_by , 
                owner = obj.book_copy.owner,
                book_copy = obj.book_copy,
                due_date = datetime.now(timezone.utc) + timedelta(days=7),
            )
            Notification.objects.create(
                notification_type = 'request_accepted',
                actor = self.request.user,
                receiver_user = obj.requested_by,
                message = f'{self.request.user} accepted your request for book {obj.book_copy.book.title}', 
                link = f'{settings.BACKEND_URL}/api/v1/borrow/records/{recordObj.id}'
            )
        if serializer.validated_data.get('status') == 'REJECTED':
            Notification.objects.create(
                notification_type = 'request_rejected',
                actor = self.request.user,
                receiver_user = obj.requested_by,
                message = f'{self.request.user} rejected your request for book {obj.book_copy.book.title}',
                link = f'{settings.BACKEND_URL}/api/v1/borrow/{obj.id}'
            )
        # print("Record should be created by now")
        serializer.save()
        # return super().perform_update(serializer)
    

    

""" BorrowRecord CURD operations -------------->         """

class BorrowRecordListView(ListAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer



class SpecificBorrowRecordView(RetrieveUpdateDestroyAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    lookup_field = 'id'


""" BorrowExtensionRequest CRUD operatoins-------->   """

class BorrowExtensionRequestListView(ListCreateAPIView):
    queryset = BorrowExtensionRequest.objects.all()
    # serializer_class = ExtensionRequestSerialier

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExtensionCreateSerializer
        return ExtensionRequestSerialier


class SpecificBorrowExtensionRequestView(RetrieveUpdateAPIView):
    queryset = BorrowExtensionRequest.objects.all()
    serializer_class = ExtensionRequestSerialier
