# Generated by Django 3.2.8 on 2021-10-12 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20211012_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='boughtitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
