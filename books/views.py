from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
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

@api_view(['GET','POST'])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializers = TagSerializer(tags, many = True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        serializer = TagSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagListView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['GET', 'DELETE'])
def specific_tag(request, id):
    tag = get_object_or_404(Tag, pk = id)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpecificTagView(RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


""" Book Model CRUD ----------------->     """

class BookListView(ListCreateAPIView):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = BookSerializer

class SpecificBookView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = BookSerializer
    lookup_field = 'id'

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


""" BookCopy Model CRUD --------------->      """

class BookCopyListView(ListCreateAPIView):
    # queryset = BookCopy.objects.select_related('book').select_related('owner').all()
    serializer_class = BookCopySerializer
    
    def get_queryset(self):
        book_id = self.kwargs.get('id')
        print('Book Id :',book_id)
        return BookCopy.objects.select_related('book').prefetch_related('owner').filter(book_id = book_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCopyCreateSerializer
        return BookCopySerializer
    
    def perform_create(self, serializer):
        book_id = self.kwargs.get('id')
        serializer.save(owner = self.request.user, book_id = book_id)

class SpecificBookCopyView(RetrieveUpdateDestroyAPIView):
    # queryset = BookCopy.objects.select_related('book').select_related('owner').all()
    serializer_class = BookCopySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        book_id = self.kwargs.get('bookId')
        return BookCopy.objects.select_related('book').prefetch_related('owner').filter(book_id = book_id)
        # return super().get_queryset()

class BookCopyViewSet(ModelViewSet):
    lookup_field='pk'

    def get_queryset(self):
        if self.action == 'list':
            pass
        if self.action == 'retrieve':
            pass
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            pass
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)

""" BookReview Model CRUD --------------->      """

class BookReviewListView(ListCreateAPIView):
    # queryset = BookReview.objects.all()
    # serializer_class = BookReviewSerializer

    def get_queryset(self):
        bookId = self.kwargs.get('id')
        return BookReview.objects.filter(book_id = bookId )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookReviewCreateSerializer
        return BookReviewSerializer
    
    def perform_create(self, serializer):
        bookId = self.kwargs.get('id')
        bookObj = get_object_or_404(Book,pk = bookId)
        serializer.save(user = self.request.user, book = bookObj)

class SpecificBookReviewView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookReviewSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        bookId = self.kwargs.get('bookId')
        return BookReview.objects.filter(book_id = bookId)
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return BookReviewCreateSerializer
        return BookReviewSerializer


class BookReviewViewSet(ModelViewSet):

    def get_queryset(self):
        return super().get_queryset()
    
    def get_serializer_class(self):
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)