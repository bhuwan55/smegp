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


class ExamUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = (
            'start_date',
            'end_date',
            'exam_type',
        )

    def update(self, instance ,validated_data):
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.exam_type = validated_data.get('exam_type', instance.exam_type)
        instance.save()
        return instance
    
    def validate(self, data, *args):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date>end_date:
            raise serializers.ValidationError("Start date must be less than end date")
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