from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from borrow.models import BorrowRequest, BorrowRecord
from borrow.serializers import BorrowRequestSerializer, BorrowRecordSerializer, RequestCreateSerializer
# Create your views here.

class BorrowRequestListView(ListCreateAPIView):
    queryset = BorrowRequest.objects.all()
    # serializer_class = BorrowRequestSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RequestCreateSerializer
        return BorrowRequestSerializer
        
    def perform_create(self, serializer):
        serializer.save(requested_by = self.request.user)

class SpecificBorrowRequestView(RetrieveUpdateDestroyAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    lookup_field = 'id'

class BorrowRecordListView(ListAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer



class SpecificBorrowRecordView(RetrieveUpdateDestroyAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    lookup_field = 'id'
