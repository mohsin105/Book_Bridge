from django.urls import path, include
from rest_framework_nested import routers
from books.views import CategoryViewSet, BookViewSet, BookCopyViewSet, BookReviewViewSet
from borrow.views import BorrowRequestViewSet, BorrowRecordViewSet, BorrowExtensionRequestViewSet

router = routers.DefaultRouter()

router.register('categories',CategoryViewSet)
router.register('books', BookViewSet)

book_router = routers.NestedDefaultRouter(router, 'books', lookup = 'book') # '/books/<int:book_id>/

book_router.register('reviews', BookReviewViewSet, basename='reviews')
book_router.register('copies', BookCopyViewSet, basename='copies')

# router.register('books', ViewSetName)

urlpatterns = [
    path('books/', include('books.urls')),
    path('borrow/', include('borrow.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('', include(book_router.urls))
]
