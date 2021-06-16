from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserLoginView, UserRegistrationView, UserLogoutView, AdminRegistrationView, \
                                AdminLoginView, ParentRegistrationView, ParentLoginView, SponserRegistrationView, \
                                    SponserLoginView, StaffRegistrationView, StaffLoginView, UserUpdateDeleteView

app_name = "account"


urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/<int:pk>/', UserUpdateDeleteView.as_view(), name='update'),

    path('register/admin', AdminRegistrationView.as_view(), name='register_admin'),
    path('login/admin', AdminLoginView.as_view(), name='login_admin'),

    path('register/parent', ParentRegistrationView.as_view(), name='register_parent'),
    path('login/parent', ParentLoginView.as_view(), name='login_parent'),

    path('register/sponser', SponserRegistrationView.as_view(), name='register_student'),
    path('login/sponser', SponserLoginView.as_view(), name='login_sponser'),

    path('register/staff', StaffRegistrationView.as_view(), name='register_staff'),
    path('login/staff', StaffLoginView.as_view(), name='login_staff'),
]