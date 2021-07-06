import datetime
from rest_framework import serializers
from .models import Exam
from grade.models import Grade
from django.core.exceptions import ValidationError


class ExamCreateSerializer(serializers.ModelSerializer):
    grade_id = serializers.IntegerField()
    class Meta:
        model = Exam
        fields = (
            'start_date',
            'end_date',
            'exam_type',
            'grade_id'
        )

    def create(self, validated_data):
        grade_id = validated_data.get('grade_id')
        grade = Grade.objects.get(id=grade_id)
        exam = Exam.objects.create(grade=grade,start_date=validated_data.get('start_date'),\
            end_date=validated_data.get('end_date'),exam_type=validated_data.get('exam_type'))
        return exam
    def validate(self,data,**args):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date>end_date:
            raise serializers.ValidationError("Start date must be less than end date")
        return data


class ExamViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Exam
        fields = (
            'id',
            'start_date',
            'end_date',
            'exam_type',
            'grade_id'
        )
        read_only_fields = ['id',]
    def create(self,validated_data):
        grade = Grade.objects.get(id=validated_data.get('grade_id'))
        exam = grade.exam.all()
        return exam
    
    def update(self, instance ,validated_data):
        print("hello")
        exam = Exam.objects.get(id=validated_data['id'])
        exam.start_date = validated_data.get('start_date', exam.start_date)
        exam.end_date = validated_data.get('end_date', exam.end_date)
        exam.exam_type = validated_data.get('exam_type', exam.exam_type)
        return exam
    
    def validate(self, data, *args):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date>end_date:
            raise serializers.ValidationError("Start date must be less than end date")
        try:
            exam = Exam.objects.get(id=data['id'])
        except Exam.DoesNotExist:
            raise serializers.ValidationError("No Exam of given id exists")
        return data


class ExamListSerializer(serializers.Serializer):
    grade_id = serializers.IntegerField()
    
    class Meta:
        fields = (
                'grade_id',
                )
    
    def create(self, validated_data):
        grade = Grade.objects.get(id=validated_data.get('grade_id'))
        exam = grade.exam.all()
        return exam