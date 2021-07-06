from rest_framework import permissions
from .models import AdminProfile

ALL_METHODS = ['GET','POST','DELETE','PUT', 'HEAD', 'OPTIONS','CONNECT','CONNECT']


class IsOwnerOrNo(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.id == request.user.id:
            return True


class IsOwnerOrNoROles(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.user.id == request.user.id:
            return True
        


class IsAdminOrNo(permissions.BasePermission):
    """
    Custom permission to only Admin owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print("Hello")
        if request.user.role == 1:
            profile = AdminProfile.objects.get(user = request.user)
            if profile.school.id == obj.grade.school.id:
                return True
            else:
                return False
            return True
        else:
            return False