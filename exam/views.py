from rest_framework.views import APIView
from rest_framework import generics
from django.http import Http404
from .serializers import ExamCreateSerializer, ExamListSerializer, ExamViewSerializer
from .models import Exam
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from account.models import AdminProfile
from grade.models import Grade
from .permissions import IsAdminOrNo, IsOfThisSchool


class ExamAPIView(APIView):
    serializer_class = ExamCreateSerializer
    permission_classes = (IsAuthenticated, IsOfThisSchool)

    def get(self, request):
        if request.user.role == 1:
            try:
                admin = request.user.admin
            except AdminProfile.DoesNotExist:
                message= "Please login in from Admin account not superuser"
                return Response(message)
            school = admin.school
            grades = school.grade.all()
            grade = {}
            for value in grades:
                grade[value.id] = value.name
            response={
                "school": school.id,
                "grades": grade
            }
            return Response(response)
        else:
            error = "Only admin is allowed!!!"
            return Response(error)

    def post(self, request):
        if request.user.role == 1:
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Exam successfully registered!',
                    'exam': serializer.data,
                }
                return Response(response, status=status_code)
        else:
            error = "Only admin is allowed!!!"
            return Response(error)


class ExamListAPIView(APIView):
    serializer_class = ExamListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        role = request.user.role
        if role==1:
            admin = request.user.admin
            school = admin.school
        elif role==2:
            staff = request.user.staff
            school = staff.school
        elif role == 3:
            parent = request.user.parent
            school = parent.school
        elif role == 4:
            sponser = request.user.sponser
            school = sponser.school
        else:
            response = {"error": "An error occured with user type"}
            return Response(response, status=HTTP_400_BAD_REQUEST)
        grades = school.grade.all()

        grade = {}
        for value in grades:
            grade[value.id] = value.name
        response={
            "school": school.id,
            "grades": grade,
            "user_type": role
        }
        return Response(response)
            
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            grade = Grade.objects.get(id=serializer.data.get('grade_id'))
            exams = grade.exam.all()
            E = {}
            for x in  exams:
                exam = ExamViewSerializer(x)
                E[exam.data.get('id')] = exam.data
            response = {
                'success': True,
                'message': 'Exam list!',
                'exam': E,
            }
            return Response(response)

class ExamUpdateDeleteAPIView(APIView):
    serializer_class = ExamViewSerializer
    permission_classes = (IsAuthenticated, IsAdminOrNo, IsOfThisSchool)

    def get_object(self, pk):
        try:
            obj = Exam.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Exam.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ExamViewSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save()
            response = {
                'success': True,
                'message': 'Changes Saved to Exam!',
                'exam': serializer.data,
            }
            return Response(response)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

