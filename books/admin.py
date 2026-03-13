from django.contrib import admin
from books.models import Category, Tag,Book, BookCopy
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(BookCopy)
