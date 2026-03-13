from django.urls import path, include
from rest_framework_nested import routers

router = routers.DefaultRouter()

# router.register('books', ViewSetName)

urlpatterns = [
    path('books/', include('books.urls')),
    path('borrow/', include('borrow.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]
