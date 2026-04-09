from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from books.models import Category, Tag, Book, BookCopy, BookReview
from books.serializers import CategorySerializer, TagSerializer, BookSerializer, BookCopySerializer, BookCopyCreateSerializer, BookReviewSerializer, BookReviewCreateSerializer, BookCreateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.permissions import IsAdminOrBookCopyAuthorOrReadOnly, IsAdminOrReviewAuthor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from books.filters import BookFilter
# Create your views here.

# Category Model CRUD -----------------> 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

""" Tag Model CURD --------------->     """

class TagViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

""" Book Model CRUD ----------------->     """

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    lookup_field = 'pk'
    permission_classes=[IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend , SearchFilter, OrderingFilter]
    ordering_fields = ['created_at',]
    search_fields = ['title', 'author', ]
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return BookCreateSerializer
        return BookSerializer


""" BookCopy Model CRUD --------------->      """


class BookCopyViewSet(ModelViewSet):
    lookup_field='pk'
    permission_classes=[IsAdminOrBookCopyAuthorOrReadOnly]
    filter_backends =[DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['availability_status', 'book_condition']
    ordering_fields = ['created_at']
    search_fields = ['availability_status', 'book_condition'] #look_up automatically applied on direct fields

    def get_queryset(self):
        bookId = self.kwargs.get('book_pk')
        return BookCopy.objects.select_related('book').prefetch_related('owner').filter(book_id = bookId)
        
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return BookCopyCreateSerializer
        return BookCopySerializer
    
    def perform_create(self, serializer):
        bookId = self.kwargs.get('book_pk')
        serializer.save(owner = self.request.user, book_id = bookId)

""" BookReview Model CRUD --------------->      """

class BookReviewViewSet(ModelViewSet):

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            return [IsAdminOrReviewAuthor()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        bookId =self.kwargs.get('book_pk')
        return BookReview.objects.filter(book_id = bookId)
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return BookReviewCreateSerializer
        return BookReviewSerializer
    
    def perform_create(self, serializer):
        bookId = self.kwargs.get('book_pk')
        bookObj = get_object_or_404(Book,pk = bookId)
        serializer.save(user = self.request.user, book = bookObj)