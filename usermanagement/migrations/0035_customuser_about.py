# Generated by Django 3.2.9 on 2022-06-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0034_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]