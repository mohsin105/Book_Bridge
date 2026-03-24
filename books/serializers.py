from rest_framework import serializers
from books.models import Category, Tag, Book, BookCopy ,BookReview
from users.serializers import SimpleCustomUser
from django.conf import settings

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
    
    def create(self, validated_data):
        if not validated_data.get('cover_image'):
            validated_data['cover_image'] = 'book_cover/default_cover.png'
        return super().create(validated_data)

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title',]

class BookCopySerializer(serializers.ModelSerializer):
    # book = serializers.StringRelatedField()
    book = SimpleBookSerializer()
    owner = SimpleCustomUser()
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status', 'book_condition', 'note', 'created_at', 'updated_at']
        read_only_fields = ['book','created_at', 'updated_at']

class BookCopyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'availability_status', 'book_condition', 'note']

class SimpleBookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status', 'book_condition', 'note',]

class BookReviewSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    user = SimpleCustomUser()
    class Meta:
        model = BookReview
        fields = ['id','book','user','rating', 'comment', 'created_at', 'updated_at']
        read_only_fields=['book','user','created_at', 'updated_at']

class BookReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']