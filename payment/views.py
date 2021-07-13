from rest_framework import generics
from rest_framework.views import APIView
from .serializers import CategorySerializer, CreatePaymentSerializer, ShowPaymentSerializer,\
    PaymentSerializer, ShowCategorySerializer, UpdateDeletePaymentSerializer
from .models import Category, Payment
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminOrNo
from rest_framework import status
from account.models import StudentProfile
from django.http import Http404


class CategoryApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,IsAdminOrNo,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self,request):
        grades = request.user.admin.school.grade.all()
        grade = {}
        for value in grades:
            grade[value.id] = value.name
        categories = Category.objects.filter(school=request.user.admin.school)
        if categories:
            category = {}
            for value in categories:
                x = ShowCategorySerializer(value)
                category[x.data["id"]]=x.data
            return Response({"categories":category,"grades":grade})
        else:
            return Response({"message":"No payment category available, create one","grades":grade})
            
        


class CategoryRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsAdminOrNo,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CreatePaymentView(APIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = (IsAuthenticated,IsAdminOrNo, )

    def get(self,request):
        categories = Category.objects.filter(school=request.user.admin.school)
        if categories:
            category = {}
            for value in categories:
                x = ShowCategorySerializer(value)
                category[x.data["id"]]=x.data
            return Response({"categories":category})
        else:
            return Response({"message":"No payment category available, create One"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Payment Sucessfully Created!!!',
                'detail': serializer.data,
            }

            return Response(response, status=status_code)


class UpdateDeletePaymentAPIView(APIView):
    """View for updating Payment."""
    serializer_class = UpdateDeletePaymentSerializer
    permission_classes = (IsAuthenticated,IsAdminOrNo, )

    def get_object(self, pk):
        try:
            obj = Payment.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = UpdateDeletePaymentSerializer(instance, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            data = {
                "payment": "try deleting and creating one."
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        message = "payment deleted successfully"
        return Response(message,status=status.HTTP_204_NO_CONTENT)


class ShowPaymentView(APIView):
    """To show payment for respective student."""
    serializer_class = ShowPaymentSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if (request.user.role == 2 or request.user.role == 5):
            return Response({"message":"You need permission to perform this activity."})
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            try:
                student = StudentProfile.objects.get(id=serializer.data['student_id'])
            except StudentProfile.DoesNotExist:
                return Response({"message":"No data for this student available."})
            if (request.user.role==1):
                if(request.user.admin.school!=student.grade.school):
                    return Response({"message":"Permission denied.Not allowed."})
            if(request.user.role==3):
                if(request.user.parent.school!=student.grade.school):
                    return Response({"message":"Permission denied.Not allowed."})
            if(request.user.role==4):
                if(request.user.sponser.school!=student.grade.school):
                    return Response({"message":"Permission denied.Not allowed."})
            try:
                payment = student.payment.all()
                value = {}
                for payment in payment:
                    x = PaymentSerializer(payment)
                    value[payment.id] = x.data
            except:
                return Response({"message":"No data available"})

            response = {
                'success': True,
                'message': 'payment Details',
                'payments': value,
            }

            return Response(response)