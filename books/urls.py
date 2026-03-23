from django.urls import path, include
from books.views import category_list, specific_category, tag_list, specific_tag,CategoryListView, SpecificCategoryView, TagListView, SpecificTagView, BookListView, SpecificBookView, BookCopyListView, SpecificBookCopyView, BookReviewListView, SpecificBookReviewView

urlpatterns = [
    # path('categories/', category_list),
    path('categories/', CategoryListView.as_view()),
    # path('categories/<int:id>/', specific_category),
    path('categories/<int:id>/', SpecificCategoryView.as_view()),
    # path('tags/', tag_list),
    path('tags/', TagListView.as_view()),
    # path('tags/<int:id>/', specific_tag)
    path('tags/<int:id>/', SpecificTagView.as_view()),
    path('', BookListView.as_view(), name='books'),
    path('<int:id>/', SpecificBookView.as_view(), name='book-details'),
    path('<int:id>/copies/', BookCopyListView.as_view(), name='copies' ),
    path('<int:bookId>/copies/<int:pk>/', SpecificBookCopyView.as_view(), name = 'copy-details'),
    path('<int:id>/reviews/', BookReviewListView.as_view(), name='reviews' ),
    path('<int:bookId>/reviews/<int:pk>/', SpecificBookReviewView.as_view(), name='review-details')
]
