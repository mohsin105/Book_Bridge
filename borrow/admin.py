from django.contrib import admin
from borrow.models import BorrowRequest, BorrowRecord
# Register your models here.
admin.site.register(BorrowRequest)
admin.site.register(BorrowRecord)