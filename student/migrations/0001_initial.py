# Generated by Django 2.0.6 on 2020-05-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.SmallIntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'other')])),
                ('grade', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
            ],
            options={
                'db_table': 'student',
            },
        ),
    ]
