# from rest_framework import serializers
# from .models import Exam


# class ExamCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exam
#         fields = (
#             'id',
#             'first_name',
#             'last_name',
#             'email',
#             'contact_number',
#             'address',
#             'role',
#             'edn_number',
#             'username',
#             'password',
#         )
#         read_only_fields =  ('id',)
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         auth_user = User.objects.create_user(**validated_data)
#         # auth_user.save()
#         return auth_user