from rest_framework import generics
from .serializers import GradeSerializer
from .models import Grade
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated



class GradeApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeRUDApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer