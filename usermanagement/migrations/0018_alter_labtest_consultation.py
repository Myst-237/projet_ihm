# Generated by Django 3.2.9 on 2021-12-27 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0017_auto_20211227_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='consultation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.consultation'),
        ),
    ]
