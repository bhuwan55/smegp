from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from school.models import School


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, contact_number, password, role, edn_number, first_name=None, address=None, last_name=None, alternate_contact=None):
        """Create a user"""
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have a valid email.')

        if not contact_number:
            raise ValueError('Users must have a valid contact number.')
        
        if not edn_number:
            raise ValueError('Users must have a valid EDN number.')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username,
            contact_number=contact_number,
            alternate_contact=alternate_contact,
            edn_number=edn_number,
            role=role,
            address=address
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, contact_number, edn_number, password, role):
        """Method to handle: manage.py superuser"""
        user = self.create_user(
            email=email,
            username=username,
            contact_number=contact_number,
            password=password,
            edn_number=edn_number,
            role=role,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    STAFF = 2
    PARENT = 3
    SPONSER = 4
    STUDENT = 5

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (PARENT, 'Parent'),
        (SPONSER, 'Sponser'),
        (STUDENT, 'Student'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)

    first_name = models.CharField(max_length=50,null=True, blank=True)
    last_name = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=20)
    contact_number = models.BigIntegerField(unique=True)
    alternate_contact = models.BigIntegerField(default=None, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50,null=True, blank=True)
    edn_number = models.CharField(max_length=50, unique=True)

    #django default fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'contact_number', 'edn_number', 'role']

    def __str__(self):
        return self.username


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username



class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    monthly_fee = models.DecimalField(max_digits=7, decimal_places=2,null=True, blank=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

    # grade/class detail

class SponserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sponser')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username



class StaffProfile(models.Model):

    TYPE_CHOICES = {
        (1, 'Teaching'),
        (2, 'Non-Teaching')
    }

    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)
    staff_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, blank=True, null=True, default=1)

    def __str__(self):
        return self.user.username
