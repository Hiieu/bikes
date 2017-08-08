import os
from argparse import ArgumentParser
from csv import DictReader
from datetime import datetime, timedelta

from generate import (
    DATETIME_FMT,
    FILE_NAME,
    generate_csv
)


class Average(object):
    file_name = FILE_NAME
    sum_timedelta = timedelta(0)
    rows_to_calc = 0  # rows between given period to calculate

    def __init__(self, arrival, departure):
        self.arrival, self.departure = self._format_datetime(arrival), \
                                         self._format_datetime(departure)

    def calculate(self):
        with open(self.file_name) as f:
            reader = DictReader(f, delimiter=',')
            rows = self._get_correct_rows_dates(reader)
            for row in rows:
                row_arrival, row_departure = row[0], row[1]
                self.sum_timedelta += (row_arrival - self.arrival) + \
                                      (self.departure - row_departure)

        rows_to_calc = self.rows_to_calc
        if rows_to_calc:
            average = self.sum_timedelta.total_seconds() / rows_to_calc
        else:
            average = rows_to_calc
        return str(timedelta(seconds=int(round(average))))

    def _get_correct_rows_dates(self, reader):
        """The generator which yield rows dates between given reporting period"""
        columns = reader.fieldnames  # First entry is treated as a header
        is_header = True
        for row in reader:
            if is_header:
                first_row_dates = self._get_row_dates(columns[2], columns[3])
                if first_row_dates:
                    yield first_row_dates
                is_header = False

            row_dates = self._get_row_dates(row[columns[2]], row[columns[3]])
            if row_dates:
                yield row_dates

    def _get_row_dates(self, arrival, departure):
        arrival, departure = self._format_row_dates(arrival, departure)
        if self._check_if_row_is_correct(arrival, departure):
            self.rows_to_calc += 1
            return arrival, departure

    def _check_if_row_is_correct(self, arrival, departure):
        if arrival == self.arrival and departure == self.departure:
            return False
        return self.arrival <= arrival < departure <= self.departure

    def _format_row_dates(self, arrival='', departure=''):
        """Format datetime string to datetime object
        :return: tuple of arrival and departure datetime object
        """
        if not arrival:
            arrival = self.arrival
        if not departure:
            departure = self.departure

        return self._format_datetime(arrival), self._format_datetime(departure)

    @staticmethod
    def _format_datetime(dt):
        if isinstance(dt, str):
            return datetime.strptime(dt, DATETIME_FMT)
        return dt


def handle_parser(args):
    if not os.path.exists(FILE_NAME):
        generate_csv()
    print(Average(args.start, args.end).calculate())


def create_parser():
    parser = ArgumentParser(description='Algorithm for calculating average '
                                        'journey across all bikes and stations',
                            epilog='python run.py -start 20170714T10:04:00 '
                                   '-end 20170715T13:04:00')
    parser.add_argument('-start',
                        help='Start of the reporting_period', required=True)
    parser.add_argument('-end',
                        help='End of the reporting_period', required=True)
    handle_parser(parser.parse_args())


if __name__ == "__main__":
    create_parser()
