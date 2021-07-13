from django.urls import path, include
from .views import CategoryApiView, CategoryRUDApiView, CreatePaymentView, ShowPaymentView\
    ,UpdateDeletePaymentAPIView

app_name = "payment"

urlpatterns = [
    path('category/', CategoryApiView.as_view(),name="create_category" ),
    path('category/<int:pk>/', CategoryRUDApiView.as_view(),name="RUD_category" ),

    path('', CreatePaymentView.as_view(), name="create_payment"),
    path('<int:pk>/', UpdateDeletePaymentAPIView.as_view(), name="update_delete_payment"),

    path('show/', ShowPaymentView.as_view(), name="show_payment"),
]