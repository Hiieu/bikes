""""
Script that used to Generate the `stations.csv` file.
"""

import csv
import random
from datetime import datetime
from faker import Faker

fake = Faker('en_GB')

DATETIME_FMT = '%Y%m%dT%H:%M:%S'
FILE_NAME = 'stations.csv'
FIELDNAMES = ('station_id', 'bike_id', 'arrival_datetime', 'departure_datetime')
ROWS = 300
START_DT = datetime(2017, 7, 14)
END_DT = datetime(2017, 7, 15)


def _get_fake_datetime():
    return fake.date_time_between_dates(START_DT, END_DT).strftime(DATETIME_FMT)


def get_bike_rent_period():
    arrival_datetime = '' if random.random() > 0.8 else _get_fake_datetime()
    departure_datetime = '' if random.random() > 0.8 else _get_fake_datetime()

    if arrival_datetime and departure_datetime:
        if arrival_datetime > departure_datetime:
            arrival_datetime, departure_datetime = departure_datetime, arrival_datetime
    return {
        'arrival_datetime': arrival_datetime,
        'departure_datetime': departure_datetime
    }


def _bike_id_func(bike_set):
    _id = random.randint(1, 10000)
    if _id in bike_set:
        return _bike_id_func(bike_set)
    return _id


def generate_rows():
    rows = []
    bikes_set = set()

    for n in range(ROWS):
        row = {}
        bike_id = _bike_id_func(bikes_set)
        row['bike_id'] = bike_id
        bikes_set.add(bike_id)
        row['station_id'] = random.randint(1, 1000)
        row.update(**get_bike_rent_period())
        rows.append(row)
    return rows


def generate_csv():
    with open(FILE_NAME, 'w') as fd:
        fieldnames = FIELDNAMES
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        results = generate_rows()
        random.shuffle(results)
        writer.writerows(results)

if __name__ == "__main__":
    generate_csv()
