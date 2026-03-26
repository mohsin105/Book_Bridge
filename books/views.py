from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from books.models import Category, Tag, Book, BookCopy, BookReview
from books.serializers import CategorySerializer, TagSerializer, BookSerializer, BookCopySerializer, BookCopyCreateSerializer, BookReviewSerializer, BookReviewCreateSerializer
from rest_framework import status
# Create your views here.

# Category Model CRUD -----------------> 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

""" Tag Model CURD --------------->     """

class TagViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

""" Book Model CRUD ----------------->     """

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


""" BookCopy Model CRUD --------------->      """


class BookCopyViewSet(ModelViewSet):
    lookup_field='pk'

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