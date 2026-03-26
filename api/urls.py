from django.urls import path, include
from rest_framework_nested import routers
from books.views import CategoryViewSet, BookViewSet, BookCopyViewSet, BookReviewViewSet, TagViewSet
from borrow.views import BorrowRequestViewSet, BorrowRecordViewSet, BorrowExtensionRequestViewSet

router = routers.DefaultRouter()

router.register('categories',CategoryViewSet)
router.register('books', BookViewSet)
router.register('tags', TagViewSet)
router.register('borrow/requests', BorrowRequestViewSet, basename='requests')
# router.register('records', BorrowRecordViewSet, basename='records')
router.register('borrow/records',BorrowRecordViewSet, basename='records' )
router.register('extensions', BorrowExtensionRequestViewSet,basename='extensions' )


book_router = routers.NestedDefaultRouter(router, 'books', lookup = 'book') # '/books/<int:book_id>/
record_router = routers.NestedDefaultRouter(router, 'borrow/records', lookup = 'record')

book_router.register('reviews', BookReviewViewSet, basename='reviews')
book_router.register('copies', BookCopyViewSet, basename='copies')

record_router.register('extensions', BorrowExtensionRequestViewSet, basename='record-extensions' )

urlpatterns = [
    # path('books/', include('books.urls')),
    path('borrow/', include('borrow.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('', include(book_router.urls)),
    path('', include(record_router.urls))
]
