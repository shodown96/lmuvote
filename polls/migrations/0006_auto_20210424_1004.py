# Generated by Django 3.1.4 on 2021-04-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20210423_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='cover',
            field=models.ImageField(upload_to='candidates'),
        ),
    ]
