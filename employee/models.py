from django.db import models

# Create your models here.


class Employee(models.Model):
    ch = (
        (0, 'male'),
        (1, 'female'),
        (2, 'other'),
    )

    name = models.CharField(max_length=30)
    password = models.CharField(max_length=64)
    gender = models.SmallIntegerField(choices=ch)

    class Meta:
        db_table = 'employee'

