# Generated by Django 2.0.1 on 2021-07-09 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20210708_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'unpaid'), (2, 'paid')], default=1),
        ),
    ]
