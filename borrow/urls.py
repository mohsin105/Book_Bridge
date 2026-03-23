from django.urls import path
from borrow.views import BorrowRequestListView, SpecificBorrowRequestView, BorrowRecordListView, SpecificBorrowRecordView, pending_requests,specific_pending_request,SpecificPendingRequest
# from 
urlpatterns = [
    path('', BorrowRequestListView.as_view(), name = 'requests'),
    path('<int:id>/', SpecificBorrowRequestView.as_view(), name='request-details'),
    path('records/', BorrowRecordListView.as_view(), name='records'),
    path('records/<int:id>/', SpecificBorrowRecordView.as_view(), name='record-details'),
    path('user/pending-requests/', pending_requests, name='pending-requests' ),
    path('user/pending-requests/<int:id>/', SpecificPendingRequest.as_view(), name='pending-request-details')
]
