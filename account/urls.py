from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import UserLoginView, UserRegistrationView, UserLogoutView, AdminRegistrationView, \
                                AdminLoginView, ParentRegistrationView, ParentLoginView, SponserRegistrationView, \
                                    SponserLoginView, StaffRegistrationView, StaffLoginView, UserUpdateDeleteView\
                                        ,AdminUpdateDeleteView, ParentUpdateDeleteView, SponserUpdateDeleteView,\
                                            StaffUpdateDeleteView, ChangePasswordView, StudentRegistrationView,\
                                                StudentListView, StudentAllView, StudentDetailView,\
                                                    StudentSelectView

app_name = 'account'


urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('login/', UserLoginView.as_view(), name='login'),
    # path('register/', UserRegistrationView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='reset_password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('update/<int:pk>/', UserUpdateDeleteView.as_view(), name='update'),

    path('register/admin/', AdminRegistrationView.as_view(), name='register_admin'),
    path('login/admin/', AdminLoginView.as_view(), name='login_admin'),
    path('update/admin/<int:pk>/', AdminUpdateDeleteView.as_view(), name='update_admin'),

    path('register/parent/', ParentRegistrationView.as_view(), name='register_parent'),
    path('login/parent/', ParentLoginView.as_view(), name='login_parent'),
    path('update/parent/<int:pk>/', ParentUpdateDeleteView.as_view(), name='update_parent'),

    path('register/sponser/', SponserRegistrationView.as_view(), name='register_sponser'),
    path('login/sponser/', SponserLoginView.as_view(), name='login_sponser'),
    path('update/sponser/<int:pk>/', SponserUpdateDeleteView.as_view(), name='update_sponser'),


    path('register/staff/', StaffRegistrationView.as_view(), name='register_staff'),
    path('login/staff/', StaffLoginView.as_view(), name='login_staff'),
    path('update/staff/<int:pk>/', StaffUpdateDeleteView.as_view(), name='update_staff'),

    path('register/student/', StudentRegistrationView.as_view(), name='register_student'),
    path('list/student/', StudentListView.as_view(), name="list_student"),
    path('all/student/', StudentAllView.as_view(), name="all_student"),
    path('detail/student/<int:pk>/', StudentDetailView.as_view(), name="detail_student"),
    path('select/student/', StudentSelectView.as_view(), name="select_student"),


]