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
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied

def overdue_count(user):
    return BorrowRecord.objects.filter(transaction_status='OVERDUE', borrower = user).count()

def active_record_count(user):
    return BorrowRecord.objects.filter(transaction_status='ACTIVE', borrower = user).count()

def extension_request_count(user, recordObj):
    return BorrowExtensionRequest.objects.filter(extension_status = 'ACCEPTED', requested_by = user, borrow_record = recordObj )

"""  BorrowRequest CRUD operations ---------->   """

# class BorrowRequestListView(ListCreateAPIView)

# class SpecificBorrowRequestView(RetrieveUpdateDestroyAPIView)


class BorrowRequestViewSet(ModelViewSet):
    lookup_field='pk'
    permission_classes=[IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        # swagger guard
        if getattr(self,'swagger_fake_view',False):
            return BorrowRequest.objects.none()

        if self.request.user.is_superuser:
            return BorrowRequest.objects.all().order_by('-created_at')
        return BorrowRequest.objects.filter(Q(requested_by = self.request.user) | Q(book_copy__owner = self.request.user)).order_by('-created_at')
    
    def get_serializer_class(self):
        # swagger guard
        if getattr(self, 'swagger_fake_view', False):
            return BorrowRequestSerializer
        
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
        if overdue_count(self.request.user)>0:
            raise PermissionDenied("Request Failed!! You have overdue records. Please clear dues first. ")
        
        if active_record_count(self.request.user)>=2:
            raise PermissionDenied("You cannot have more than two books at the same time")
        
        serializerStatus = serializer.validated_data.get('status')
        if serializerStatus and serializerStatus not in ['PENDING']:
            raise PermissionDenied("User can only request with status Pending")
        
        requestObj = serializer.save(requested_by = self.request.user)
        bookCopyObj = serializer.validated_data.get('book_copy')
        owner = bookCopyObj.owner
        Notification.objects.create(
            notification_type = 'borrow_request',
            actor = self.request.user,
            receiver_user = owner,
            message = f'{self.request.user} has requested {bookCopyObj.book.title} from you',
            link = f'{settings.BACKEND_URL}/api/v1/borrow/requests/{requestObj.id}'
        )
    
    def perform_update(self, serializer):
        requestObj = self.get_object()
        print('Requester Update Form: ',serializer.validated_data)
        # Borrower options-> 
        if self.request.user == requestObj.requested_by:
            # print('this is the requester')
            serializerStatus = serializer.validated_data.get('status')
            if serializerStatus and serializerStatus not in ['CANCELLED', 'PENDING']:
                # print('not pending nor cancelled')
                raise PermissionDenied("Your are not allowed to perform this operation!")
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
                    link = f'{settings.BACKEND_URL}/api/v1/borrow/requests/{requestObj.id}'
                )
            # print("Record should be created by now")
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def sent(self, request, pk=None):
        """
        List of Borrow-Requests sent by the User
        - By default: shows only Pending Requests
        - Upon query_param status = 'all' : shows all sent-requests
        """
        requestStatus = self.request.query_params.get('status')
        if requestStatus == 'all':
            qs = BorrowRequest.objects.filter(requested_by = self.request.user).order_by('-created_at')
        else:
            qs = BorrowRequest.objects.filter(requested_by = self.request.user, status = 'PENDING').order_by('-created_at')
        # serializer = self.get_serializer(qs, many = True)
        serializer = BorrowRequestSerializer(qs, many = True)
        # return Response({'message':'action checking', 'status':requestStatus})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def received(self, request, pk =None):
        """
        List of Borrow-Requests Received by the User
        - By default: shows only Pending Received-Requests
        - Upon query_param status = 'all' : shows all Received-requests
        """
        qs = BorrowRequest.objects.filter(book_copy__owner = request.user)
        # print(qs)
        requestStatus = self.request.query_params.get('status')
        if not requestStatus: #not 'all'
            qs = qs.filter(status = 'PENDING')
        
        serializer = BorrowRequestSerializer(qs, many = True)
        return Response(serializer.data)
    
    # @action(detail = True, methods=['put', 'patch'])
    # def sent_detail(self, request, pk = None):
    #     serializer = self.get_serializer(self.get_object())
    #     return Response(serializer.data)
    def list(self, request, *args, **kwargs):
        """List of Borrow-Requests related to the User->  Either Received or Sent"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Details of a single request related to the User """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Create a BorrowRequest for a Book-Copy -- Allowed to Authenticated user"""
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially Update a specific Borrow-Request. 
        - Requester can only update when the Request-status is still Pending
        - Cancel the request-status and request-message. 
        - Book-Copy Owner can change status to Accept or Reject
        - When Owner accepts a request, a Borrow-Record is automatically created
        """
        return super().partial_update(request, *args, **kwargs)
    
    


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
        if getattr(self,'swagger_fake_view',False):
            return BorrowRecord.objects.none()

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
            raise PermissionDenied("Borrower Cannot Update the Record")
        # return super().perform_update(serializer)
    
    def list(self, request, *args, **kwargs):
        """List of Borrow-Requests related to the User->  Either Borrowed or Lent"""
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Details of Specific borrow-record - related to the User"""
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Manually Create a Borrow-record: Allowed only for Admin"""
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Update a Borrow-Record
        - Only Owner can change the status to Returned
        - Admin has full access
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Update a Borrow-Record
        - Only Owner can change the status to Returned
        - Admin has full access
        """
        return super().partial_update(request, *args, **kwargs)
    



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
        if getattr(self,'swagger_fake_view',False):
            return BorrowExtensionRequest.objects.none()
        
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
        if extension_request_count(self.request.user, recordObj)>=2:
            raise PermissionDenied("Maximum 2 accepted extensions allowed. ")
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
                raise PermissionDenied("You cannot change an already Rejected request. ")
            if submittedStatus and submittedStatus not in ['CANCELLED', 'PENDING']:
                raise PermissionDenied("Your are not allowed to perform this operation!")
            serializer.save()
        
        # owner side -> 
        elif recordObj.owner == self.request.user:
            if submittedStatus and submittedStatus not in ['ACCEPTED', 'REJECTED']:
                raise PermissionDenied("Owner can only Accept or Reject the request")
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
    def list(self, request, *args, **kwargs):
        """List of BorrowExtension Request- of a specific Borrow-Record
        - Only Admin or Record owner or borrower can access
        """
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Details of a specific BorrowExtension Request- of a specific Borrow-Record
        - Only Admin or Record owner or borrower can access
        """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Create a  BorrowExtension Request for a specific Borrow-Record
        - Only the borrower of that record can create extension-request
        """
        return super().create(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially Update a specific Extension-Request. 
        - Requester can only update when the Request-status is still Pending
        - Cancel the request-status and request-message. 
        - Book-Copy Owner can change status to Accept or Reject
        - When Owner accepts a request, a Borrow-Record is automatically updated. Due-date and extension_request_count changed
        """
        return super().partial_update(request, *args, **kwargs)

# class SpecificPendingExtensionRequest(RetrieveUpdateAPIView):

