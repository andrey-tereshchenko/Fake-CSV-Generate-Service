# Generated by Django 3.1.5 on 2021-01-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0002_column_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='order',
            field=models.IntegerField(unique=True),
        ),
    ]
