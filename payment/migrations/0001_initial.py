# Generated by Django 2.0.1 on 2021-07-07 06:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_auto_20210707_0440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('category', models.ManyToManyField(related_name='detail', to='payment.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField(default=datetime.date.today)),
                ('total_payed_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('payment_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='payment.Detail')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='account.StudentProfile')),
            ],
        ),
    ]
