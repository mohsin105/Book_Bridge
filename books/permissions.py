from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrBookCopyAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or request.user == obj.owner

class IsAdminOrReviewAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff or request.user == obj.user
