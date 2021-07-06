from rest_framework import permissions
from account.models import AdminProfile, StaffProfile, ParentProfile, SponserProfile

ALL_METHODS = ['GET','POST','DELETE','PUT', 'HEAD', 'OPTIONS','CONNECT','CONNECT']


class IsAdminOrNo(permissions.BasePermission):
    """
    Custom permission to only Admin owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, school):
        if request.user.role == 1:
            profile = AdminProfile.objects.get(user = request.user)
            if profile.school.id == school.id:
                return True
            else:
                return False
            return True
        else:
            return False


class IsOfThisSchool(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 1:
            profile = AdminProfile.objects.get(user = request.user)

        elif request.user.role == 2:
            profile = StaffProfile.objects.get(user = request.user)

        elif request.user.role == 3:
            profile = ParentProfile.objects.get(user = request.user)

        elif request.user.role == 4:
            profile = SponserProfile.objects.get(user = request.user)

        if profile.school.id == obj.school.id:
            return True
        else:
            return False