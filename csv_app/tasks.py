from __future__ import absolute_import, unicode_literals

import os
import random
import csv

from celery import shared_task
from faker import Faker
from django.core.files import File

from csv_app.models import *

faker = Faker()


def get_data_by_type(type, range=None):
    data = ''
    if type == ColumnType.NAME:
        data = faker.name()
    elif type == ColumnType.JOB:
        data = faker.job()
    elif type == ColumnType.ADDRESS:
        data = faker.address()
    elif type == ColumnType.PHONE:
        data = faker.phone_number()
    elif type == ColumnType.INT:
        range_from = range[0]
        range_to = range[1]
        data = faker.random_int(range_from, range_to)
    elif type == ColumnType.TEXT:
        range_from = range[0]
        range_to = range[1]
        data = ' '.join([word for word in faker.words(random.randint(range_from, range_to))])
    elif type == ColumnType.DATE:
        data = faker.date_of_birth()
    elif type == ColumnType.COMPANY:
        data = faker.company()
    elif type == ColumnType.EMAIL:
        data = faker.email()
    elif type == ColumnType.DOMAIN:
        data = faker.domain_name()
    return data


def get_delimiter_by_type(type):
    delimiter = ' '
    if type == SeparatorType.COMMA:
        delimiter = ','
    elif type == SeparatorType.POINT:
        delimiter = '.'
    elif type == SeparatorType.SEMICOLON:
        delimiter = ';'
    return delimiter


def get_quote_type(type):
    quote = '\''
    if type == QuoteType.DOUBLE_QUOTE:
        quote = '\"'
    return quote


@shared_task
def generate_csv_file(data_set_id, num_rows):
    dataset = DataSet.objects.filter(id=data_set_id).first()
    columns = list(set(dataset.schema.column_set.all()))
    columns = sorted(columns, key=lambda column: column.order)
    delimiter = get_delimiter_by_type(dataset.schema.column_separator)
    quotechar = get_quote_type(dataset.schema.string_character)
    with open('dataset_{}.csv'.format(data_set_id), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar)
        writer.writerow([column.name for column in columns])
        for i in range(num_rows):
            row = [get_data_by_type(column.type, (column.range_from, column.range_to)) if column.type in (
                ColumnType.INT, ColumnType.TEXT) else get_data_by_type(column.type) for column in columns]
            writer.writerow(row)
    f = open('dataset_{}.csv'.format(data_set_id))
    dataset.file = File(f)
    dataset.status = Status.COMPLETED
    os.remove('dataset_{}.csv'.format(data_set_id))
    dataset.save()
