from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)


class Department(BaseModel):
    dep_name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.dep_name

    class Meta:
        db_table = 'bz_department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name


class Employees(BaseModel):
    gender_choices = (
        (0, 'male'),
        (1, 'female'),
        (2, 'secret')
    )

    emp_name = models.CharField(max_length=128)
    gender = models.SmallIntegerField(choices=gender_choices)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    dep = models.ForeignKey(to=Department,
                            on_delete=models.CASCADE,
                            related_name='employees',
                            db_constraint=False)

    @property
    def dep_name(self):
        return self.dep.dep_name

    @property
    def gender_name(self):
        return self.get_gender_display()

    def __str__(self):
        return self.emp_name

    class Meta:
        db_table = 'employees'
        verbose_name = '员工'
        verbose_name_plural = verbose_name
