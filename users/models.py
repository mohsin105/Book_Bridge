from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from users.managers import CustomUserManager
from cloudinary.models import CloudinaryField
# from borrow.models import BorrowRecord #this line causes circular import error. 
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=18, blank=True, null=True)
    profile_image = CloudinaryField(
        'image',
        folder = 'profile_images',
        blank=True, 
        null=True,
        default='profile_images/default_profile'
    )
    # profile_image = models.ImageField(upload_to='profile_images/',blank=True, null=True, default='profile_images/default_profile.jpg')
    rating  = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1),MaxValueValidator(5)],
        blank=True
    )
    late_return = models.IntegerField(default=0, blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class UserReview(models.Model):
#     reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_user_list')
#     reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
#     borrow_record = models.ForeignKey(BorrowRecord, on_delete=models.CASCADE,related_name='review_list')
#     rating = models.PositiveIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.reviewed_by.first_name} reviewing {self.reviewed_user.first_name} on {self.borrow_record.book_copy.book.title}"


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('borrow_request','Borrow Request'),
        ('request_accepted','Request Accepted'),
        ('request_rejected','Request Rejected'),
        ('book_returned','Book Returned'),
        ('extension_request','Extension Request'),
        ('extension_accepted','Extension Accepted'),
        ('review_received','Review Received'),
    )

    notification_type = models.CharField(max_length=40, choices=NOTIFICATION_TYPE)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.CharField(max_length=260, blank=True, null=True)
    is_read = models.BooleanField(blank=True ,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.notification_type} from {self.actor} to {self.receiver_user}'