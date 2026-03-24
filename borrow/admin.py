from django.contrib import admin
from borrow.models import BorrowRequest, BorrowRecord, BorrowExtensionRequest
# Register your models here.
admin.site.register(BorrowRequest)
admin.site.register(BorrowRecord)
admin.site.register(BorrowExtensionRequest)