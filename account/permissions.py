from rest_framework import permissions

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

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.user.id == request.user.id:
            return True
        

        # Write permissions are only allowed to the owner of the snippet.