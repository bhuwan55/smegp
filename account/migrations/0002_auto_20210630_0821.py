# Generated by Django 2.0.1 on 2021-06-30 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='school',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade.Grade'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sponserprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sponser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL),
        ),
    ]