# Generated by Django 2.0.1 on 2021-07-25 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_school_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='unique_id',
            field=models.CharField(blank=True, editable=False, max_length=6, unique=True),
        ),
    ]
