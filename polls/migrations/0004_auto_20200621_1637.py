# Generated by Django 3.0.5 on 2020-06-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200620_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='candidates'),
        ),
        migrations.AddField(
            model_name='movie',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='movies/'),
        ),
    ]
