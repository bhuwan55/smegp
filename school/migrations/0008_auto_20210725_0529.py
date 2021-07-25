# Generated by Django 2.0.1 on 2021-07-25 05:29

from django.db import migrations, models
import school.models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20210725_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='unique_id',
            field=models.CharField(blank=True, default=school.models.create_new_ref_number, max_length=6, unique=True),
        ),
    ]
