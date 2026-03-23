from django.contrib import admin
from books.models import Category, Tag,Book, BookCopy, BookReview
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(BookReview)