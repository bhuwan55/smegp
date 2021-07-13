from rest_framework.views import APIView
from rest_framework import generics
from .serializers import GradeCreateSerializer
from .models import Grade
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .permissions import IsAdminOrNo
from school.models import School


class GradeApiView(APIView):
    serializer_class = GradeCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminOrNo)

    def get(self,request):
        response = {
                'status': status.HTTP_200_OK,
                'school_id': request.user.admin.school.id,
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            school = School.objects.get(id = serializer.validated_data["school_id"])
            self.check_object_permissions(self.request, school)
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Grade successfully registered!',
                'grade': serializer.data,
            }

            return Response(response, status=status_code)