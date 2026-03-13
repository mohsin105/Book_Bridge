from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=1,null=True ,related_name='books')
    tags = models.ManyToManyField(Tag, related_name='book_list')
    author = models.CharField(max_length=100)
    description = models.TextField()
    page_count = models.PositiveIntegerField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_cover/', blank=True, null=True, default='book_cover/default_cover.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    AVAILABILITY_STATUS = (
        ('AVAILABLE','Available'),
        ('BORROWED','Borrowed'),
        ('RESERVED','Reserved'),
        ('UNAVAILABLE','Unavailable'),
    )
    BOOK_CONDITION = (
        ('NEW','New'),
        ('GOOD','Good'),
        ('OLD','Old'),
    )
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='copies')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='owned_books')
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_STATUS, default='AVAILABLE')
    book_condition = models.CharField(max_length=10, choices=BOOK_CONDITION, default='NEW')
    note=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner.first_name} copy of {self.book.title}'



class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='comments')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            userName = self.user.first_name
        else:
            userName = 'Deleted User'
        return f"{userName}'s comment on {self.book.title}"
    