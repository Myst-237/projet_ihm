# Generated by Django 3.2.9 on 2021-11-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0011_auto_20211126_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorreport',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='doctorreport',
            name='modified',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='patientvitalcard',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='patientvitalcard',
            name='modified',
            field=models.DateTimeField(),
        ),
    ]