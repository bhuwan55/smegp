# Generated by Django 2.0.1 on 2021-06-30 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20210615_0605'),
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School'),
            preserve_default=False,
        ),
    ]
