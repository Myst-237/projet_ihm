# Generated by Django 3.2.9 on 2021-12-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0022_auto_20211229_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]