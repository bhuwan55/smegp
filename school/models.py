from django.db import models


class School(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)


    def __str__(self):
        return self.name