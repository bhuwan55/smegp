from django.db import models
import random




class School(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    unique_id = models.CharField(
           max_length = 6,
           blank=True,
           unique=True,
      )

    def __str__(self):
        return self.name