from rest_framework import serializers

from emp.models import Employees


class EmployeesViewSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        rst = Employees.objects.filter(emp_name=attrs.get('emp_name'))
        if rst:
            raise serializers.ValidationError('员工已存在')
        return attrs

    class Meta:
        model = Employees
        fields = ('id', 'emp_name', 'gender', 'gender_name', 'salary', 'dep', 'dep_name')
        extra_kwargs = {
            'dep_name': {
                'read_only': True
            },
            'dep': {
                'write_only': True
            },
            'gender_name': {
                'read_only': True
            },
            'gender': {
                'write_only': True
            },
            'id': {
                'read_only': True
            }
        }
