# Generated by Django 3.1.5 on 2021-01-24 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0004_auto_20210124_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(),
        ),
    ]
