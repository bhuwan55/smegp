from django.db import models
import random

def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_id = str(random.randint(1000,9999))
        if not School.objects.filter(unique_id=unique_id):
            not_unique = False
    return unique_id


class School(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    unique_id = models.CharField(
           max_length = 6,
           blank=True,
           unique=True,
        #    default=create_new_ref_number,
      )

    def __str__(self):
        return self.name