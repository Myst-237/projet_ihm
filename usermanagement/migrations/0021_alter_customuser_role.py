# Generated by Django 3.2.9 on 2021-12-29 08:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0020_auto_20211229_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient'), ('Receptionist', 'Receptionist'), ('Admin', 'Admin'), ('Accountant', 'Accountant'), ('Nurse', 'Nurse'), ('Labtech', 'Labtech'), ('HRM', 'HRM'), ('Specialist', 'Specialist')], max_length=50), blank=True, default=list, null=True, size=None),
        ),
    ]