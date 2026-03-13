from django.urls import path
from borrow.views import BorrowRequestListView, SpecificBorrowRequestView, BorrowRecordListView, SpecificBorrowRecordView
# from 
urlpatterns = [
    path('', BorrowRequestListView.as_view(), name = 'requests'),
    path('<int:id>/', SpecificBorrowRequestView.as_view(), name='request-details'),
    path('records/', BorrowRecordListView.as_view(), name='records'),
    path('records/<int:id>/', SpecificBorrowRecordView.as_view(), name='record-details')
]
