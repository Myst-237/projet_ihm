# Generated by Django 3.2.9 on 2021-11-26 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0009_auto_20211126_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='modified',
            field=models.DateTimeField(),
        ),
    ]
