from rest_framework import permissions
from account.models import AdminProfile


class IsAdminOrNo(permissions.BasePermission):
    """
    Custom permission to only Admin owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.role == 1:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 1:
            profile = AdminProfile.objects.get(user = request.user)
            return True
        else:
            return False