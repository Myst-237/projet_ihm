# Generated by Django 3.2.9 on 2021-12-27 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0014_auto_20211227_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorreport',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='doctorreport',
            name='patient',
        ),
        migrations.AddField(
            model_name='doctorreport',
            name='consultation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usermanagement.consultation'),
        ),
    ]
