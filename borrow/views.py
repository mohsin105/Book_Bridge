from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from datetime import timedelta,datetime, timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from borrow.models import BorrowRequest, BorrowRecord,BorrowExtensionRequest
from borrow.serializers import BorrowRequestSerializer, BorrowRecordSerializer, RequestCreateSerializer, RequestPatchSerializer, ExtensionRequestSerialier, ExtensionCreateSerializer, ExtensionPatchSerializer, RecordUpdateSerializer
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from users.models import Notification
from books.models import BookCopy
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser,IsAuthenticated
from borrow.permissions import IsAdminOrRecordOwner

"""  BorrowRequest CRUD operations ---------->   """

# class BorrowRequestListView(ListCreateAPIView)

# class SpecificBorrowRequestView(RetrieveUpdateDestroyAPIView)


class BorrowRequestViewSet(ModelViewSet):
    lookup_field='pk'
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(Q(requested_by = self.request.user) | Q(book_copy__owner = self.request.user))
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            obj = self.get_object()
            # Requested Option ---> 
            if self.request.user == obj.requested_by:
                return RequestCreateSerializer #For requester to cancel the status, that field must be in serializer
            # Owner Option ----> 
            elif self.request.user == obj.book_copy.owner:
                return RequestPatchSerializer
        if self.request.method == "POST":
            return RequestCreateSerializer  #No need for status field here. 
        return BorrowRequestSerializer
            
        # if self.request.method in ['POST','PUT']:
    
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
    
    def perform_update(self, serializer):
        requestObj = self.get_object()
        # print('Requester Update Form: ',serializer.validated_data)
        # Borrower options-> 
        if self.request.user == requestObj.requested_by:
            # print('this is the requester')
            serializerStatus = serializer.validated_data.get('status')
            if serializerStatus and serializerStatus not in ['CANCELLED', 'PENDING']:
                # print('not pending nor cancelled')
                return Response(status = status.HTTP_403_FORBIDDEN)
            serializer.save()
        
        # Owner Options  -> 
        if self.request.user == requestObj.book_copy.owner:
            if serializer.validated_data.get('status')=='ACCEPTED':
                recordObj = BorrowRecord.objects.create(
                    borrower = requestObj.requested_by , 
                    owner = requestObj.book_copy.owner,
                    book_copy = requestObj.book_copy,
                    due_date = datetime.now(timezone.utc) + timedelta(days=7),
                )
                Notification.objects.create(
                    notification_type = 'request_accepted',
                    actor = self.request.user,
                    receiver_user = requestObj.requested_by,
                    message = f'{self.request.user} accepted your request for book {requestObj.book_copy.book.title}', 
                    link = f'{settings.BACKEND_URL}/api/v1/borrow/records/{recordObj.id}'
                )
            if serializer.validated_data.get('status') == 'REJECTED':
                Notification.objects.create(
                    notification_type = 'request_rejected',
                    actor = self.request.user,
                    receiver_user = requestObj.requested_by,
                    message = f'{self.request.user} rejected your request for book {requestObj.book_copy.book.title}',
                    link = f'{settings.BACKEND_URL}/api/v1/borrow/{requestObj.id}'
                )
            # print("Record should be created by now")
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def sent(self, request, pk=None):
        requestStatus = self.request.query_params.get('status')
        if requestStatus == 'all':
            qs = BorrowRequest.objects.filter(requested_by = self.request.user)
        else:
            qs = BorrowRequest.objects.filter(requested_by = self.request.user, status = 'PENDING')
        # serializer = self.get_serializer(qs, many = True)
        serializer = BorrowRequestSerializer(qs, many = True)
        # return Response({'message':'action checking', 'status':requestStatus})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def received(self, request, pk =None):
        qs = BorrowRequest.objects.filter(book_copy__owner = request.user)
        print(qs)
        requestStatus = self.request.query_params.get('status')
        if not requestStatus: #not 'all'
            qs = qs.filter(status = 'PENDING')
        
        serializer = BorrowRequestSerializer(qs, many = True)
        return Response(serializer.data)
    
    # @action(detail = True, methods=['put', 'patch'])
    # def sent_detail(self, request, pk = None):
    #     serializer = self.get_serializer(self.get_object())
    #     return Response(serializer.data)


# def pending_requests(request):

# def specific_pending_request(request, id):


# class SpecificPendingRequest(RetrieveUpdateAPIView):
    

    

""" BorrowRecord CURD operations -------------->         """

class BorrowRecordViewSet(ModelViewSet):
    # queryset = BorrowRecord.objects.all()
    # serializer_class = BorrowRecordSerializer
    lookup_field = 'pk'
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['borrower', 'owner']

    def get_permissions(self):
        if self.request.method in ['POST','DELETE']:
            return [IsAdminUser()]
        if self.request.method in ['PUT','PATCH']:
            return [IsAdminOrRecordOwner()] #Only Owner|Admin can update the record
        return [IsAuthenticated()]

    def get_queryset(self):
        qs= BorrowRecord.objects.filter(Q(borrower = self.request.user) | Q(owner = self.request.user))
        recordStatus = self.request.query_params.get('status')
        if recordStatus=='active': #not all, only active ones
            qs = qs.filter(transaction_status = 'ACTIVE')
        return qs
    
    def get_serializer_class(self):
        if self.request.method in ['PUT']:
            return RecordUpdateSerializer
        return BorrowRecordSerializer
    
    def perform_update(self, serializer):
        recordObj = self.get_object()
        # Only Owner can update the Record
        if self.request.user == recordObj.owner:
            serializer.save()
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        # return super().perform_update(serializer)


""" BorrowExtensionRequest CRUD operatoins-------->   """

# class BorrowExtensionRequestListView(ListCreateAPIView):


# class SpecificBorrowExtensionRequestView(RetrieveUpdateAPIView):

class BorrowExtensionRequestViewSet(ModelViewSet):
    lookup_field = 'pk'
    http_method_names = ['get', 'post','patch',  'head', 'options', 'trace']
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['extension_status', 'requested_by', 'borrow_record__owner']
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recordObj = self.kwargs.get('record_pk')
        user = self.request.user
        qs = BorrowExtensionRequest.objects.filter(
            Q(requested_by = user) | Q(borrow_record__owner = user)
        )
        if recordObj:
            qs = BorrowExtensionRequest.objects.filter(borrow_record = recordObj)
        
        return qs
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExtensionCreateSerializer
        if self.request.method == 'PATCH':
            return ExtensionPatchSerializer
        return ExtensionRequestSerialier
    
    # Only by the borrower -> 
    def perform_create(self, serializer):
        recordId = self.kwargs.get('record_pk')
        recordObj = get_object_or_404(BorrowRecord, pk = recordId)
        requested_date = recordObj.due_date + timedelta(days=7)
        requestObj=serializer.save(
            requested_by = self.request.user, 
            borrow_record = recordObj, 
            requested_due_date = requested_date
        )
        Notification.objects.create(
            notification_type = 'extension_request',
            actor = self.request.user,
            receiver_user = recordObj.owner,
            message = f'{self.request.user} requesting extension for {recordObj.book_copy.book.title}',
            link = f'{settings.BACKEND_URL}/api/v1/borrow/records/{recordId}/extensions/{requestObj.id}/'
        )
    
    def perform_update(self, serializer):
        requestObj = self.get_object()
        recordObj = requestObj.borrow_record
        print(serializer.validated_data)
        submittedStatus = serializer.validated_data.get('extension_status')
        # borrower side
        if requestObj.requested_by == self.request.user:
            if requestObj.extension_status == 'REJECTED':
                return Response(status= status.HTTP_403_FORBIDDEN)
            if submittedStatus and submittedStatus not in ['CANCELLED', 'PENDING']:
                return Response(status = status.HTTP_403_FORBIDDEN)
            serializer.save()
        
        # owner side -> 
        elif recordObj.owner == self.request.user:
            if submittedStatus and submittedStatus not in ['ACCEPTED', 'REJECTED']:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if serializer.validated_data.get('extension_status') == 'ACCEPTED':
                recordObj.extension_request_count += 1
                recordObj.due_date = requestObj.requested_due_date
                recordObj.save()
                Notification.objects.create(
                    notification_type = 'extension_accepted',
                    actor = self.request.user,
                    receiver_user = requestObj.requested_by,
                    message = f'{self.request.user} accpeted extension request for {recordObj.book_copy.book.title}',
                    link = f'{settings.BACKEND_URL}/api/v1/borrow/records/{recordObj.id}/'
                )
            if serializer.validated_data.get('extension_status') == 'REJECTED':
                Notification.objects.create(
                    notification_type = 'request_rejected',
                    actor = self.request.user,
                    receiver_user = requestObj.requested_by,
                    message = f'{self.request.user} rejected your extension request for {recordObj.book_copy.book.title}',
                    link = f'{settings.BACKEND_URL}/api/v1/borrow/records/{recordObj.id}/'
                )
            serializer.save()
        # return super().perform_update(serializer)

# class SpecificPendingExtensionRequest(RetrieveUpdateAPIView):

