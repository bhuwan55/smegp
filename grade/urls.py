from django.urls import path
from .views import GradeApiView

app_name = "grade"

urlpatterns = [
    path('', GradeApiView.as_view(),name="create_grade" ),

]
