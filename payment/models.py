from django.db import models
from datetime import date
from account.models import StudentProfile
from school.models import School
from grade.models import Grade


class Category(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2,null=True, blank=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name="category")
    grade = models.ForeignKey('grade.Grade', on_delete=models.DO_NOTHING, related_name="category")


class Payment(models.Model):
    CHOICES = (
        (1, 'unpaid'),
        (2, 'paid'),
    )
    status = models.PositiveSmallIntegerField(choices=CHOICES, default=1)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2,null=True, blank=True)
    date = models.DateField(default=date.today)
    category = models.ManyToManyField('Category', related_name="detail")
    student = models.ForeignKey('account.StudentProfile', on_delete=models.CASCADE, related_name="payment")