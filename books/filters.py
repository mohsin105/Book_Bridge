from django_filters.rest_framework import FilterSet
from books.models import Book, BookCopy

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields={
            'title':['icontains'],
            'category_id' : ['exact'],
            'author': ['icontains']
        }