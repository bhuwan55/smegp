from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from .models import User, AdminProfile, ParentProfile, StaffProfile, SponserProfile, StudentProfile
from django.contrib.auth import authenticate, login
from grade.models import Grade
from school.models import  School
from .sendmail import SendVerificationMail
from django.core.exceptions import ValidationError
from grade.serializers import GradeShowSerializer


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
        # auth_user.save()
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
            'email': {'validators': []},
            'contact_number': {'validators': []}
        }

    def update(self, instance ,validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.address = validated_data.get('address', instance.address)
        instance.username = validated_data.get('username', instance.username)
        # instance.save()
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
        if user.role==3:
            is_approved = user.parent.is_approved
        elif user.role==2:
            is_approved = user.staff.is_approved
        elif user.role==4:
            is_approved = user.sponser.is_approved
        elif user.role==1:
            is_approved = True
        elif user.role==5:
            raise serializers.ValidationError("No login for student")
        if is_approved==False:
            raise serializers.ValidationError("Your Account needs to be Approved by Admin to login!!!")
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


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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
            user.save()
        user = User.objects.get(username=user.validated_data['username'])

        school_id = validated_data.get('school_id')
        school = School.objects.get(id = school_id)

        admin = AdminProfile.objects.create(user=user, school=school)
        user.role = 1
        user.save()
        return admin


class AdminUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = AdminProfile
        fields = (
            'user',
        )

    def update(self, instance ,validated_data):
        return instance
    
    def validate(self, validated_data, *args):
        user_data = validated_data['user']
        email = user_data["email"]
        contact = user_data['contact_number']
        email_exists = User.objects.filter (email=email).exclude(id=self.instance.user.pk) # excluding the current user from queryset
        if self.instance.user and self.instance.user.pk and not email_exists:
            contact_exists = User.objects.filter (contact_number=contact).exclude(pk=self.instance.user.pk)
            if not contact_exists:
                user = User.objects.get(id=self.instance.user.id)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)

                user.email = user_data.get('email', user.email)
                user.contact_number = user_data.get('contact_number', user.contact_number)
                user.address = user_data.get('address', user.address)
                user.username = user_data.get('username', user.username)
                user.save()
                validation = {
                'email': email,
                'contact_number': contact
            }
                return validation
            else:
                raise ValidationError("User with this Contact Number already exists")
        else:
            raise ValidationError("User with this Email already exists")




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


class ParentUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = ParentProfile
        fields = (
            'user',
        )

    def update(self, instance ,validated_data):
        return instance
    
    def validate(self, validated_data, *args):
        user_data = validated_data['user']
        email = user_data["email"]
        contact = user_data['contact_number']
        email_exists = User.objects.filter (email=email).exclude (id=self.instance.user.pk) # excluding the current user from queryset
        if self.instance.user and self.instance.user.pk and not email_exists:
            contact_exists = User.objects.filter (contact_number=contact).exclude (pk=self.instance.user.pk)
            if not contact_exists:
                user = User.objects.get(id=self.instance.user.id)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)

                user.email = user_data.get('email', user.email)
                user.contact_number = user_data.get('contact_number', user.contact_number)
                user.address = user_data.get('address', user.address)
                user.username = user_data.get('username', user.username)
                user.save()
                validation = {
                'email': email,
                'contact_number': contact
            }
                return validation
            else:
                raise ValidationError("User with this Contact Number already exists")
        else:
            raise ValidationError("User with this Email already exists")


class ParentSerializer(serializers.ModelSerializer):
    """To view parent detail"""
    user = UserUpdateSerializer()

    class Meta:
        model = ParentProfile
        fields = "__all__"
        extra_fields = ('id',)


class ParentApproveSerializer(serializers.Serializer):
    parent_id = serializers.IntegerField()
    class Meta:
        fields = {'parent_id',}


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


class SponserUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = SponserProfile
        fields = (
            'user',
        )

    def update(self, instance ,validated_data):
        return instance
    
    def validate(self, validated_data, *args):
        user_data = validated_data['user']
        email = user_data["email"]
        contact = user_data['contact_number']
        email_exists = User.objects.filter (email=email).exclude (id=self.instance.user.pk) # excluding the current user from queryset
        if self.instance.user and self.instance.user.pk and not email_exists:
            contact_exists = User.objects.filter (contact_number=contact).exclude (pk=self.instance.user.pk)
            if not contact_exists:
                user = User.objects.get(id=self.instance.user.id)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)

                user.email = user_data.get('email', user.email)
                user.contact_number = user_data.get('contact_number', user.contact_number)
                user.address = user_data.get('address', user.address)
                user.username = user_data.get('username', user.username)
                user.save()
                validation = {
                'email': email,
                'contact_number': contact
            }
                return validation
            else:
                raise ValidationError("User with this Contact Number already exists.")
        else:
            raise ValidationError("User with this Email already exists.")


class SponserSerializer(serializers.ModelSerializer):
    """To view sponser detail"""
    user = UserUpdateSerializer()

    class Meta:
        model = SponserProfile
        fields = "__all__"
        extra_fields = ('id',)


class SponserApproveSerializer(serializers.Serializer):
    sponser_id = serializers.IntegerField()
    class Meta:
        fields = {'sponser_id',}


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


class StaffUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = StaffProfile
        fields = (
            'user',
            'staff_type',
            'monthly_salary',
        )

    def update(self, instance ,validated_data):
        return instance

    def validate(self, validated_data, *args):
        self.instance.monthly_salary = validated_data.get('monthly_salary', self.instance.monthly_salary)
        self.instance.save()
        user_data = validated_data['user']
        email = user_data["email"]
        contact = user_data['contact_number']
        email_exists = User.objects.filter (email=email).exclude (id=self.instance.user.pk) # excluding the current user from queryset
        if self.instance.user and self.instance.user.pk and not email_exists:
            contact_exists = User.objects.filter (contact_number=contact).exclude (pk=self.instance.user.pk)
            if not contact_exists:
                user = User.objects.get(id=self.instance.user.id)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)

                user.email = user_data.get('email', user.email)
                user.contact_number = user_data.get('contact_number', user.contact_number)
                user.address = user_data.get('address', user.address)
                user.username = user_data.get('username', user.username)
                user.save()
                validation = {
                'email': email,
                'contact_number': contact
            }
                return validation
            else:
                raise ValidationError("User with this Contact Number already exists.")
        else:
            raise ValidationError("User with this Email already exists.")


class StaffSerializer(serializers.ModelSerializer):
    """To view staff detail"""
    user = UserUpdateSerializer()

    class Meta:
        model = StaffProfile
        fields = "__all__"
        extra_fields = ('id',)


class StaffApproveSerializer(serializers.Serializer):
    staff_id = serializers.IntegerField()
    class Meta:
        fields = {'staff_id',}


class StudentRegisterSerializer(serializers.ModelSerializer):
    grade_id = serializers.IntegerField()
    parent_id = serializers.IntegerField()
    user = UserRegistrationSerializer()
    class Meta:
        model = StudentProfile
        fields = ('user', 'grade_id','parent_id')

    def create(self, validated_data):
        grade_id = validated_data.get('grade_id')
        try:
            grade = Grade.objects.get(id = grade_id)
        except Grade.DoesNotExist:
            raise serializers.ValidationError("Grade with given Id doesnot Exists.")
        
        user = UserRegistrationSerializer(data=validated_data.get('user'))
        valid = user.is_valid(raise_exception=True)
        if valid:
            user.save()
        user = User.objects.get(username=user.validated_data['username'])
        parent = ParentProfile.objects.get(id = validated_data['parent_id'])

        student = StudentProfile.objects.create(user=user, grade=grade, monthly_fee=0,parent=parent)
        user.role = 5
        user.save()
        return student


class StudentSerializer(serializers.ModelSerializer):
    """To view Student detail"""
    user = UserUpdateSerializer()

    class Meta:
        model = StudentProfile
        fields = "__all__"
        extra_fields = ('id',)


class StudentApproveSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    class Meta:
        fields = {'student_id',}


class StudentListSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    id = serializers.IntegerField()
    grade = GradeShowSerializer()
    class Meta:
        model = StudentProfile
        fields = "__all__"
        extra_fields = ('id',)


class SelectStudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = StudentProfile
        fields = ["id",]
