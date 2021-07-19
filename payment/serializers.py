from .models import Category, Payment
from rest_framework import serializers
from account.models import StudentProfile
from django.core.exceptions import ValidationError
from grade.models import Grade


class CategorySerializer(serializers.ModelSerializer):
    """serializer  to create category """
    grade_id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ['name',"amount","grade_id"]
    
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user                             #to acess request.user in serializer
        school = user.admin.school
        grade = Grade.objects.get(id=validated_data['grade_id'])
        category = Category.objects.create(school=school,grade=grade ,**validated_data)
        return category


class ShowCategorySerializer(serializers.ModelSerializer):
    """Serializer to convert category to Json"""
    id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ["id","name","amount","grade"]
        read_only_fields = ['id',]
        depth = 1



class CategoryChooseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ['id']


class CreatePaymentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    category = CategoryChooseSerializer(many=True, read_only=False)
    class Meta:
        model = Payment
        fields = ["status","total_amount","date","category","student_id"]
        read_only_fields=['id']

    def create(self, validated_data):
        category = validated_data['category']
        student = StudentProfile.objects.get(id=validated_data['student_id'])
        payment = Payment.objects.create(total_amount=validated_data['total_amount'], date=validated_data['date'],student=student\
            ,status=validated_data['status'])
        for value in category:
            try:
                i = Category.objects.get(id=value['id'])
            except Category.DoesNotExist:
                raise serializers.ValidationError("No category with given details Exists.")
            payment.category.add(i)
        payment.save()
        return payment


class ShowPaymentSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = ["student_id"]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer to make payment object in Json. """
    id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['id',]
        depth=1

class UpdateDeletePaymentSerializer(serializers.ModelSerializer):
    """Serializer to update Payment"""

    class Meta:
        model = Payment
        fields = ('status','total_amount','date','student','category')
        depth = 1
    def update(self, instance ,validated_data):
        return instance
