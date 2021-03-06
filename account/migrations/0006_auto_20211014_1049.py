# Generated by Django 3.2.8 on 2021-10-14 03:49

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rank',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Bronze'), (2, 'Silver'), (3, 'Gold')], default=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
