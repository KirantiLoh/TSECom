# Generated by Django 3.2.8 on 2021-10-11 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_product_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review',
            field=models.CharField(default='', max_length=500),
        ),
    ]
