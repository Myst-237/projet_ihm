# Generated by Django 3.2.9 on 2021-12-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0018_alter_labtest_consultation'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='admitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('On Hold', 'On Hold')], max_length=50),
        ),
    ]
