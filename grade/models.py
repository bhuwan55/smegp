from django.db import models
from school.models import School


class Grade(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name="grade")

    def __str__(self):
        return str(self.name +" of "+ self.school.name)