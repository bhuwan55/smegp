# Generated by Django 2.0.1 on 2021-07-12 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210712_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='sponser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student', to='account.SponserProfile'),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='staff_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Teaching'), (2, 'Non-Teaching')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='account.ParentProfile'),
        ),
    ]
