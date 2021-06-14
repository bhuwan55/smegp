from django.contrib import admin
from .models import User, AdminProfile, ParentProfile, StudentProfile, SponserProfile, StaffProfile


admin.site.register(User)
admin.site.register(AdminProfile)
admin.site.register(ParentProfile)
admin.site.register(StudentProfile)
admin.site.register(SponserProfile)
admin.site.register(StaffProfile)


