from django.contrib import admin
from .models import User, AdminProfile, ParentProfile, StudentProfile, SponserProfile, StaffProfile
from rest_framework_simplejwt import token_blacklist


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)


admin.site.register(User)
admin.site.register(AdminProfile)
admin.site.register(ParentProfile)
admin.site.register(StudentProfile)
admin.site.register(SponserProfile)
admin.site.register(StaffProfile)


