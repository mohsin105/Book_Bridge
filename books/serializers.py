from rest_framework import serializers
from books.models import Category, Tag, Book, BookCopy

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['id', 'name', 'description']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title', 'category', 'tags', 'author', 'page_count', 'description', 'cover_image']


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status', 'book_condition', 'note', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BookCopyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'availability_status', 'book_condition', 'note']

class SimpleBookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status', 'book_condition', 'note',]
        