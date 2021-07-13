from .models import Grade
from rest_framework import serializers
from django.core.exceptions import ValidationError
from school.models import School


class GradeCreateSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField()

    class Meta:
        model = Grade
        fields = ['school_id','name']

    def create(self, validated_data):
        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)
        grade = Grade.objects.create(school=school,name=validated_data.get('name'))
        return grade

    def validate(self,data,**args):
        school_id = data['school_id']
        try:
            school = School.objects.get(id = school_id)
        except School.DoesNotExist:
            raise serializers.ValidationError("School with this id doesnot exists.")
        try:
            grades = school.grade.all()
        except:
            return data
        for grade in grades:
            if grade.name == data['name']:
                raise serializers.ValidationError("Grade with same name cannot Exists")
        return data


class GradeShowSerializer(serializers.ModelSerializer):
    """ used to show grade with student list"""
    id = serializers.IntegerField()
    class Meta:
        model = Grade
        fields = ['id','name',]
