from django.db import models
from users.models import User
from books.models import Book, BookCopy
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class BorrowRequest(models.Model):
    REQUEST_STATUS = (
        ('PENDING','Pending'),
        ('ACCEPTED','Accepted'),
        ('REJECTED','Rejected'),
        ('CANCELLED','Cancelled')
    )
    book_copy = models.ForeignKey(BookCopy,on_delete=models.SET_NULL,null=True, related_name='requests')
    requested_by  = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='borrow_requests')
    status = models.CharField(max_length=15, choices=REQUEST_STATUS, default='PENDING')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requested_by.first_name}'s to borrow {self.book_copy.book.title} from {self.book_copy.owner}"


class BorrowRecord(models.Model):
    STATUS = (
        ('ACTIVE','Active'),
        ('RETURNED','Returned'),
        ('OVERDUE','Overdue'),
    )
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,related_name='borrow_history')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='lending_history')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.SET_NULL,null=True, related_name = 'borrow_records')
    transaction_status = models.CharField(max_length=12, choices=STATUS, default='ACTIVE')
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True)
    returned_date = models.DateTimeField(blank=True, null= True)
    extension_request_count = models.IntegerField(
        default=0,
        blank=True,
        validators=[MinValueValidator(0),MaxValueValidator(2)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.book_copy is not None:
            if self.book_copy.book is not None:
                bookTitle = self.book_copy.book.title
        else:
            bookTitle = None
        
        if self.owner:
            ownerName = self.owner.first_name
        else:
            ownerName = 'Deleted User'
        
        if self.borrower:
            borrowerName = self.borrower.first_name
        else:
            borrowerName = 'Deleted User'

        return f'{bookTitle} record from {ownerName} to {borrowerName}'


class BorrowExtensionRequest(models.Model):
    REQUEST_STATUS = (
        ('PENDING','Pending'),
        ('ACCEPTED','Accepted'),
        ('REJECTED','Rejected'),
        ('CANCELLED','Cancelled')
    )
    requested_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='extension_requests')
    borrow_record = models.ForeignKey(BorrowRecord, on_delete=models.CASCADE, related_name='extension_request_list')
    extension_status = models.CharField(max_length=15, choices=REQUEST_STATUS, default='PENDING')
    requested_due_date = models.DateTimeField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.requested_by.first_name} on {self.borrow_record}'
