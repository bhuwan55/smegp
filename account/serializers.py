from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from .models import User, AdminProfile, ParentProfile, StaffProfile, SponserProfile
from django.contrib.auth import authenticate, login
from school.models import  School



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'address',
            'role',
            'edn_number',
            'username',
            'password',
        )
        read_only_fields =  ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        auth_user.save()
        return auth_user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'address',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance ,validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.address = validated_data.get('address', instance.address)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance



class UserLoginSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data, *args):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
                'username': user.username,
                'id': user.id
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")



class AdminRegisterSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField()
    user = UserRegistrationSerializer()
    class Meta:
        model = AdminProfile
        fields = ('user', 'school_id')

    def create(self, validated_data):
        user = UserRegistrationSerializer(data=validated_data.get('user'))
        valid = user.is_valid(raise_exception=True)
        if valid:
            user.role = 3
            user.save()
        user = User.objects.get(username=user.validated_data['username'])

        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)

        admin = AdminProfile.objects.create(user=user, school=school)
        user.role = 1
        user.save()
        return admin



class ParentRegisterSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField()
    user = UserRegistrationSerializer()
    class Meta:
        model = ParentProfile
        fields = ('user', 'school_id')

    def create(self, validated_data):
        user = UserRegistrationSerializer(data=validated_data.get('user'))
        valid = user.is_valid(raise_exception=True)
        if valid:
            user.save()
        user = User.objects.get(username=user.validated_data['username'])

        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)

        parent = ParentProfile.objects.create(user=user, school=school)
        user.role = 3
        user.save()
        return parent



class SponserRegisterSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField()
    user = UserRegistrationSerializer()
    class Meta:
        model = SponserProfile
        fields = ('user', 'school_id')

    def create(self, validated_data):
        user = UserRegistrationSerializer(data=validated_data.get('user'))
        valid = user.is_valid(raise_exception=True)
        if valid:
            user.save()
        user = User.objects.get(username=user.validated_data['username'])

        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)

        sponser = SponserProfile.objects.create(user=user, school=school)
        user.role = 4
        user.save()
        return sponser



class StaffRegisterSerializer(serializers.ModelSerializer):
    staff_type = serializers.IntegerField()
    school_id = serializers.IntegerField()
    user = UserRegistrationSerializer()
    class Meta:
        model = StaffProfile
        fields = ('user', 'school_id','staff_type')

    def create(self, validated_data):
        user = UserRegistrationSerializer(data=validated_data.get('user'))
        valid = user.is_valid(raise_exception=True)
        if valid:
            user.save()
        user = User.objects.get(username=user.validated_data['username'])

        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)

        staff = StaffProfile.objects.create(user=user, school=school, staff_type=validated_data.get('staff_type')\
            , monthly_salary=0)
        user.role = 2
        user.save()
        return staff