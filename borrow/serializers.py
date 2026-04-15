from rest_framework import serializers
from borrow.models import BorrowRequest, BorrowRecord,BorrowExtensionRequest
from books.serializers import SimpleBookCopySerializer
from users.serializers import SimpleCustomUser

class BorrowRequestSerializer(serializers.ModelSerializer):
    book_copy = SimpleBookCopySerializer()
    requested_by = SimpleCustomUser()
    status_display = serializers.SerializerMethodField(method_name='get_status_display')
    class Meta:
        model = BorrowRequest
        fields = ['id','book_copy', 'requested_by', 'status','status_display', 'message', 'created_at', 'updated_at']
        read_only_fields = ['requested_by']
    
    def get_status_display(self, obj):
        return obj.get_status_display()

class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id','book_copy','status', 'message', 'created_at', 'updated_at']
        # read_only_fields = ['requested_by']

class RequestPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'status']


class BorrowRecordSerializer(serializers.ModelSerializer):
    borrower = SimpleCustomUser()
    owner = SimpleCustomUser()
    book_copy = SimpleBookCopySerializer()
    transaction_status_display = serializers.SerializerMethodField(method_name='get_transaction_status_display')
    class Meta:
        model = BorrowRecord
        fields = ['id', 'borrower','owner', 'book_copy', 'transaction_status', 'transaction_status_display','borrow_date', 'due_date', 'returned_date', 'extension_request_count', 'created_at', 'updated_at']
        read_only_fields=['id', 'borrower','owner', 'book_copy', 'borrow_date', 'due_date', 'extension_request_count', 'created_at', 'updated_at']
        # read_only_fields = ['__all__']
    
    def get_transaction_status_display(self, obj):
        return obj.get_transaction_status_display()

class RecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields =['id', 'transaction_status']



class ExtensionRequestSerialier(serializers.ModelSerializer):
    class Meta:
        model = BorrowExtensionRequest
        fields = ['id', 'requested_by', 'borrow_record','extension_status','requested_due_date','message','created_at']
        read_only_fields=['id', 'requested_by', 'borrow_record','requested_due_date',]

class ExtensionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowExtensionRequest
        fields =['id','message']

class ExtensionPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowExtensionRequest
        fields =['id','extension_status', 'message']