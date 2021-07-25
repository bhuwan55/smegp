# Generated by Django 2.0.1 on 2021-07-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20210725_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='staff_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2, 'Non-Teaching'), (1, 'Teaching')], default=1, null=True),
        ),
    ]