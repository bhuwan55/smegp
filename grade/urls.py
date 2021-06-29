from django.urls import path, include
from .views import GradeApiView, GradeRUDApiView

app_name = "grade"

urlpatterns = [
    path('grade/', SchoolApiView.as_view(),name="create_read_school" ),
    path('school/<int:pk>/', SchoolRUDApiView.as_view(),name="view_school" ),
    path('', ChooseSchoolView.as_view(),name="choose_school" ),

    path('school/user/', include('account.urls')),

]
