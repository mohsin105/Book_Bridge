from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from books.models import Category, Tag, Book, BookCopy
from books.serializers import CategorySerializer, TagSerializer, BookSerializer, BookCopySerializer, BookCopyCreateSerializer
from rest_framework import status
# Create your views here.

# Category Model CRUD -----------------> 
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many = True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        serializer = CategorySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    

@api_view(['GET', 'DELETE'])
def specific_category(request,id):
    category = get_object_or_404(Category,pk=id)

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecificCategoryView(RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


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

class BookView(ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


""" BookCopy Model CRUD --------------->      """

class BookCopyListView(ListCreateAPIView):
    queryset = BookCopy.objects.select_related('book').select_related('owner').all()
    serializer_class = BookCopySerializer
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCopyCreateSerializer
        return BookCopySerializer
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class SpecificBookCopyView(RetrieveUpdateDestroyAPIView):
    queryset = BookCopy.objects.select_related('book').select_related('owner').all()
    serializer_class = BookCopySerializer
    lookup_field = 'copy_id'