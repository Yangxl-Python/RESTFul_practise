from django.db import models

# Create your models here.


class Student(models.Model):
    gender_choices = (
        (0, 'male'),
        (1, 'female'),
        (2, 'other'),
    )
    grade_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

    name = models.CharField(max_length=30)
    gender = models.SmallIntegerField(choices=gender_choices)
    grade = models.SmallIntegerField(choices=grade_choices)

    class Meta:
        db_table = 'student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
