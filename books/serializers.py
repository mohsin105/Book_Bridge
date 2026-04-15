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
    cover_image = serializers.ImageField()
    category = CategorySerializer()
    tags = TagSerializer(many = True)
    class Meta:
        model = Book
        fields = ['id','title', 'category', 'tags', 'author', 'page_count', 'description', 'cover_image']
    
    

class BookCreateSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Book
        fields = ['id','title','category', 'tags', 'author', 'page_count', 'description', 'cover_image']
    
    def create(self, validated_data):
        if not validated_data.get('cover_image'):
            # validated_data['cover_image'] = 'book_cover/default_cover.png'
            validated_data['cover_image'] = 'https://res.cloudinary.com/dxfk4kicy/image/upload/q_auto/f_auto/v1775883474/default_cover_szywna.png'
        return super().create(validated_data)

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title',]

class BookCopySerializer(serializers.ModelSerializer):
    # book = serializers.StringRelatedField()
    book = SimpleBookSerializer()
    owner = SimpleCustomUser()
    availability_status_display = serializers.SerializerMethodField(method_name='get_availability_status_display')
    book_condition_display = serializers.SerializerMethodField(method_name='get_book_condition_display')
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status','availability_status_display', 'book_condition','book_condition_display', 'note', 'created_at', 'updated_at']
        read_only_fields = ['book','created_at', 'updated_at']
    
    def get_availability_status_display(self, obj):
        return obj.get_availability_status_display()
    
    def get_book_condition_display(self,obj):
        return obj.get_book_condition_display()

class BookCopyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'availability_status', 'book_condition', 'note']

class SimpleBookCopySerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    owner = SimpleCustomUser()
    availability_status_display = serializers.SerializerMethodField(method_name='get_availability_status_display')
    book_condition_display = serializers.SerializerMethodField(method_name='get_book_condition_display')
    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'owner', 'availability_status','availability_status_display', 'book_condition','book_condition_display', 'note',]
    
    def get_availability_status_display(self, obj):
        return obj.get_availability_status_display()
    
    def get_book_condition_display(self,obj):
        return obj.get_book_condition_display()


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