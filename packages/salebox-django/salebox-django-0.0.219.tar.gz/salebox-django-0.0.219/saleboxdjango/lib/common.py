import datetime
import hashlib
import math
import pytz
import re
import time

from django.conf import settings
from django.db import connection
from django.utils.timezone import localtime


def api_auth():
    epoch = int(math.floor(time.time()))
    hash_str = '%s.%s.%s' % (
        settings.SALEBOX['API']['KEY'],
        settings.SALEBOX['API']['LICENSE'],
        epoch
    )

    return {
        'pos': settings.SALEBOX['API']['KEY'],
        'epoch': epoch,
        'hash': hashlib.sha256(hash_str.encode('utf-8')).hexdigest(),
        'software_type': 'salebox_django',
        'software_version': '0.0.219'
    }

def dictfetchall(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def fetchflatlist(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall()]

def fetchsinglevalue(sql):
    return fetchflatlist(sql)[0]

def get_rating_display(score, vote_count):
    if vote_count > 0:
        return {
            '100': score,
            '5': round(score / 20),
            '10': round(score / 10)
        }
    else:
        return {'100': 0, '5': 0, '10': 0}

def json_to_datetime_local(value):
    return localtime(json_to_datetime_utc(value))

def json_to_datetime_utc(value):
    return datetime.datetime(*value, tzinfo=pytz.UTC)

def update_natural_sort(model, str_column, sort_column):
    # retrieve all rows
    rows = list(model.objects.values('id', str_column, sort_column))

    # update string to be sortable
    for row in rows:
        row[str_column] = row[str_column].lower()
        row[str_column] = row[str_column].strip()
        row[str_column] = re.sub(r'^the\s+', '', row[str_column])
        row[str_column] = re.sub(r'\d+', lambda x: '%08d' % (int(x.group(0)),), row[str_column])

    # sort the values
    rows = sorted(rows, key=lambda k: k[str_column])

    # update the database records that need it
    for i, row in enumerate(rows):
        if i != row[sort_column]:
            model.objects.filter(id=row['id']).update(**{sort_column: i})
