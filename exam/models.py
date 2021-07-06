from django.db import models
from datetime import date
from grade.models import Grade
from django.db.models.signals import pre_save


class Exam(models.Model):
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    exam_type = models.CharField(max_length=100,null=True, blank=True)
    grade = models.ForeignKey('grade.Grade', on_delete=models.CASCADE, related_name="exam")

    def __str__(self):
        return str(self.exam_type + " of " + self.grade.name)


def check_date(sender, instance, *args, **kwargs):
    if instance.start_date > instance.end_date:
        raise ValueError('Start date must be less than end date')

pre_save.connect(check_date, sender=Exam)

