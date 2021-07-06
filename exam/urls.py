from django.urls import path
from .views import ExamAPIView, ExamListAPIView, ExamUpdateDeleteAPIView

app_name = "exam"

urlpatterns = [
    path('', ExamAPIView.as_view(), name="create_exam"),
    path('view/', ExamListAPIView.as_view(), name="view_exam"),
    path('update/<int:pk>/', ExamUpdateDeleteAPIView.as_view(), name="update_exam"),
]