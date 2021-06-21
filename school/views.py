from rest_framework import generics
from .serializers import SchoolSerializer, ChooseSchoolSerializer
from .models import School
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated



class SchoolApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class ChooseSchoolView(APIView):
    """ Please provide School Id """
    serializer_class = ChooseSchoolSerializer
    permission_classes = (AllowAny, )


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            id = serializer.validated_data['id']
            try:
                school = School.objects.get(id=id)
            except School.DoesNotExist:
                error = "school does not exists"
                return Response(error)
            data = {
            "school":school.name,
            }
        return Response(data)

