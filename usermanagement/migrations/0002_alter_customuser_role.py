# Generated by Django 3.2.9 on 2021-11-22 14:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('NoRole', 'NoRole'), ('Doctor', 'Doctor'), ('Patient', 'Patient'), ('Receptionist', 'Receptionist'), ('Admin', 'Admin'), ('Accountant', 'Accountant'), ('Nurse', 'Nurse'), ('Labtech', 'Labtech'), ('HRM', 'HRM'), ('Specialist', 'Specialist')], default='NoRole', max_length=50), default=list, size=None),
        ),
    ]
