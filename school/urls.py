from django.urls import path, include
from .views import SchoolApiView, SchoolRUDApiView, ChooseSchoolView

app_name = "school"

urlpatterns = [
    path('school/', SchoolApiView.as_view(),name="create_read_school" ),
    path('school/<int:pk>/', SchoolRUDApiView.as_view(),name="view_school" ),
    path('', ChooseSchoolView.as_view(),name="choose_school" ),

    path('school/user/', include('account.urls')),
    path('school/grade/', include('grade.urls')),
    path('school/exam/', include('exam.urls')),

]
