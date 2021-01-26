from datetime import date

from django.db import models
from django.contrib.auth.models import User


class ColumnType(models.TextChoices):
    NAME = 'NM', 'Full name'
    JOB = 'JB', 'Job'
    EMAIL = 'EM', 'Email'
    DOMAIN = 'DM', 'Domain'
    PHONE = 'PH', 'Phone number'
    COMPANY = 'CM', 'Company'
    TEXT = 'TX', 'Text'
    INT = 'IN', 'Integer'
    ADDRESS = 'AD', 'Address'
    DATE = 'DT', 'Date'


class SeparatorType(models.TextChoices):
    COMMA = 'C', 'Comma (,)'
    POINT = 'P', 'Point (.)'
    SEMICOLON = 'S', 'Semicolon (;)'


class QuoteType(models.TextChoices):
    DOUBLE_QUOTE = 'D', 'Double-quote (")'
    SINGLE_QUOTE = 'S', 'Single quote (\')'


class Status(models.TextChoices):
    COMPLETED = 'CMP', 'Completed'
    PROCESSING = 'PRC', 'Processing'


class Schema(models.Model):
    name = models.CharField(max_length=100)
    modified = models.DateField(default=date.today)
    column_separator = models.CharField(
        max_length=1,
        choices=SeparatorType.choices,
    )
    string_character = models.CharField(
        max_length=1,
        choices=QuoteType.choices,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=2,
        choices=ColumnType.choices,
    )
    range_from = models.IntegerField(default=None, null=True, blank=True)
    range_to = models.IntegerField(default=None, null=True, blank=True)
    order = models.IntegerField()
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)


class DataSet(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.SET_NULL, null=True)
    created = models.DateField(default=date.today)
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PROCESSING
    )
    file = models.FileField(blank=True, upload_to='csv/', null=True)
