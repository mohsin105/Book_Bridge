from rest_framework import serializers
from borrow.models import BorrowRequest, BorrowRecord,BorrowExtensionRequest
from books.serializers import SimpleBookCopySerializer
class BorrowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowRequest
        fields = ['id','book_copy', 'requested_by', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['requested_by']

class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id','book_copy', 'message', 'created_at', 'updated_at']
        # read_only_fields = ['requested_by']

class RequestPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'status']


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'borrower','owner', 'book_copy', 'transaction_status', 'borrow_date', 'due_date', 'returned_date', 'extension_request_count', 'created_at', 'updated_at']
        # read_only_fields = ['__all__']

        read_only_fields=['id', 'borrower','owner', 'book_copy', 'borrow_date', 'due_date', 'extension_request_count', 'created_at', 'updated_at']


class ExtensionRequestSerialier(serializers.ModelSerializer):
    class Meta:
        model = BorrowExtensionRequest
        fields = ['id', 'requested_by', 'borrow_record','extension_status','requested_due_date','message','created_at']

class ExtensionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowExtensionRequest
        fields =['requested_due_date','message',]