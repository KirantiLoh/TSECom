# Generated by Django 3.2.8 on 2021-10-08 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='subtotal',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
    ]
