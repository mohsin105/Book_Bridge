from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrRecordOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_staff or request.user == obj.owner
        return request.user.is_staff