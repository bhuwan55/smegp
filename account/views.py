from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserLoginSerializer, UserRegistrationSerializer, \
    AdminRegisterSerializer,ParentRegisterSerializer, SponserRegisterSerializer,\
        StaffRegisterSerializer, UserUpdateSerializer, AdminUpdateDeleteSerializer,\
            ParentUpdateDeleteSerializer, SponserUpdateDeleteSerializer, StaffUpdateDeleteSerializer,\
                ChangePasswordSerializer, StudentRegisterSerializer, StudentListSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, AdminProfile, ParentProfile, SponserProfile, StaffProfile, StudentProfile
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .permissions import IsOwnerOrNo, IsOwnerOrNoROles
from .sendmail import SendVerificationMail
from grade.models import Grade


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class UserUpdateDeleteView(APIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrNo,)


    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = UserUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            user = User.objects.get(id=serializer.validated_data['id'])
            login(request,user)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'username': serializer.data['username'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logout(request)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            user_data = serializer.data['user']
            user = User.objects.get(username=user_data['username'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Admin successfully registered!',
                'admin': serializer.data,
                'admin_id': user.admin.id
            }

            return Response(response, status=status_code)


class AdminUpdateDeleteView(APIView):
    serializer_class = AdminUpdateDeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrNoROles)


    def get_object(self, pk):
        try:
            obj = AdminProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except AdminProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = AdminUpdateDeleteSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            data = {
                "admin": serializer.data,
                "admin_id": pk
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        user = User.objects.get(id=instance.user.id)
        user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            user = User.objects.get(id=serializer.validated_data['id'])
            if user.role != 1:
                message = "please go to respective login form"
                return Response(message)
            login(request,user)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'admin_id': user.admin.id,
                    'username': serializer.data['username'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)


class ParentRegistrationView(APIView):
    serializer_class = ParentRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            user = serializer.validated_data['user']
            SendVerificationMail.send_mail(user)
            user = User.objects.get(username=user['username'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Parent successfully registered! we will mail you when we review your information',
                'parent': serializer.data,
                'parent_id': user.parent.id
            }

            return Response(response, status=status_code)



class ParentUpdateDeleteView(APIView):
    serializer_class = ParentUpdateDeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrNoROles)

    def get_object(self, pk):
        try:
            obj = ParentProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return ParentProfile.objects.get(pk=pk)
        except ParentProfile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ParentUpdateDeleteSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            data = {
                "parent": serializer.data,
                "parent_id": pk
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        user = User.objects.get(id=instance.user.id)
        user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParentLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            user = User.objects.get(id=serializer.validated_data['id'])
            if user.role != 3:
                message = "please go to respective login form"
                return Response(message)
            login(request,user)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'parent_id': user.parent.id,
                    'username': serializer.data['username'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)



class SponserRegistrationView(APIView):
    serializer_class = SponserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            user = serializer.validated_data['user']
            SendVerificationMail.send_mail(user)
            user = User.objects.get(username=user['username'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Sponser successfully registered! we will mail you when we review your information',
                'sponser': serializer.data,
                'sponser_id': user.sponser.id
            }

            return Response(response, status=status_code)


class SponserUpdateDeleteView(APIView):
    serializer_class = SponserUpdateDeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrNoROles)

    def get_object(self, pk):
        try:
            obj = SponserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return SponserProfile.objects.get(pk=pk)
        except SponserProfile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = SponserUpdateDeleteSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            data = {
                "sponser" : serializer.data,
                "sponser_id": pk
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        user = User.objects.get(id=instance.user.id)
        user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SponserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            user = User.objects.get(id=serializer.validated_data['id'])
            if user.role != 4:
                message = "This Form is Only For Sponser"
                return Response(message)
            login(request,user)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'sponser_id': user.sponser.id,
                    'username': serializer.data['username'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)



class StaffRegistrationView(APIView):
    serializer_class = StaffRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            user = serializer.validated_data['user']
            SendVerificationMail.send_mail(user)
            user = User.objects.get(username=user['username'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Staff successfully registered! we will mail you when we review your information',
                'staff': serializer.data,
                'staff_id': user.staff.id
            }

            return Response(response, status=status_code)
        

class StaffUpdateDeleteView(APIView):
    serializer_class = StaffUpdateDeleteSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrNoROles)

    def get_object(self, pk):
        try:
            obj = StaffProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return StaffProfile.objects.get(pk=pk)
        except StaffProfile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = StaffUpdateDeleteSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            data = {
                "staff": serializer.data,
                "staff_id": pk
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        user = User.objects.get(id=instance.user.id)
        user.delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            user = User.objects.get(id=serializer.validated_data['id'])
            if user.role != 2:
                message = "This Form is Only For Staff"
                return Response(message)
            login(request,user)

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'authenticatedUser': {
                    'staff_id': user.staff.id,
                    'username': serializer.data['username'],
                    'role': serializer.data['role'],
                }
            }

            return Response(response, status=status_code)


class StudentRegistrationView(APIView):
    serializer_class = StudentRegisterSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            parent = request.user.parent
        except:
            error = "You donot have permission."
            return Response(error)
        school = parent.school
        grades = school.grade.all()
        grade={}
        for value in grades:
            grade[value.id]=value.name
        return Response({
            "grades": grade,
            "parent_id": parent.id,
            "school_id": school.id
        })


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            user = serializer.validated_data['user']
            # SendVerificationMail.send_mail(user)
            user = User.objects.get(username=user['username'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Student successfully registered!, we will review data of the student.',
                'staff': serializer.data,
                'staff_id': user.student.id
            }

            return Response(response, status=status_code)


class StudentListView(APIView):
    """View to show student list for payment"""
    serializer_class = StudentListSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if (request.user.role == 2 or request.user.role == 5):
            return Response({"message":"You don't have permission"})
        if request.user.role ==1:
            school = request.user.admin.school
            grade = school.grade.all()
            grades = {}
            for grade in grade:
                students = []
                student = grade.student.all()
                for student in student:
                    x = StudentListSerializer(student)
                    students.append(x.data)
                x = grade.name
                grades[x] = students
            return Response({"grades": grades})
        if request.user.role == 3:
            student = request.user.parent.student.all()
            students = []
            for student in student:
                x = StudentListSerializer(student)
                students.append(x.data)
            return Response({"students": students})
        if request.user.role == 4:
            student = request.user.sponser.student.all()
            students = []
            for student in student:
                x = StudentListSerializer(student)
                students.append(x.data)
            return Response({"students": students})


class StudentAllView(APIView):
    """this view is to show sponser list of students"""
    serializer_class = StudentListSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user.role == 4:
            grade = request.user.sponser.school.grade.all()
            grades = {}
            for grade in grade:
                students = []
                student = grade.student.all()
                for student in student:
                    x = StudentListSerializer(student)
                    students.append(x.data)
                x = grade.name
                grades[x] = students
            return Response({"grades": grades})
        else:
            return Response({"message":"You don't have permission."})


class StudentDetailView(APIView):
    serializer_class = StudentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            obj = StudentProfile.objects.get(pk=pk)
            return obj
        except StudentProfile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        if request.user.role == 1:
            instance = self.get_object(pk)
            if request.user.admin.school == instance.grade.school:
                student = StudentListSerializer(instance)
                return Response({"student_detail":student.data})
            else:
                return Response({"message":"You don't have permission."})
        elif request.user.role == 4:
            instance = self.get_object(pk)
            if request.user.sponser.school == instance.grade.school:
                student = StudentListSerializer(instance)
                return Response({"student_detail":student.data})
            else:
                return Response({"message":"You don't have permission."})
        else:
            return Response({"message":"You don't have permission."})