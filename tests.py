from copy import deepcopy
from csv import DictWriter
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch, PropertyMock

from generate import FIELDNAMES
from run import Average, DATETIME_FMT
from tempfile import mkstemp


TEST_DATA = [{
    'station_id': 536,
    'bike_id': 8845,
    'arrival_datetime': '20170714T09:00:00',
    'departure_datetime': '20170714T12:00:00'
}, {
    'station_id': 293,
    'bike_id': 2800,
    'arrival_datetime': '20170714T08:00:00',
    'departure_datetime': '20170714T13:00:00'
}]


class TestAverageDuration(TestCase):
    def _generate_test_csv(self, test_data):
        with open(self.filename, 'w') as fd:
            fieldnames = FIELDNAMES
            writer = DictWriter(fd, fieldnames=fieldnames)
            writer.writerows(test_data)

    def setUp(self):
        self.arrival = '20170714T06:00:00'
        self.departure = '20170714T14:00:00'
        self.filename = mkstemp(suffix='.csv')[1]
        self.file_mock = patch.object(Average, 'file_name',
                                      new_callable=PropertyMock,
                                      return_value=self.filename)

    def test(self):
        self._generate_test_csv(TEST_DATA)
        with self.file_mock:
            calculated = Average(self.arrival, self.departure).calculate()
            self.assertEqual(calculated, '4:00:00')

    def test_empty_arrival(self):
        test_data = deepcopy(TEST_DATA)
        test_data[0]['arrival_datetime'] = ''
        test_data[1]['arrival_datetime'] = ''
        self._generate_test_csv(test_data)
        with self.file_mock:
            calculated = Average(self.arrival, self.departure).calculate()
            self.assertEqual(calculated, '1:30:00')

    def test_empty_dates(self):
        test_data = deepcopy(TEST_DATA)
        test_data[0]['arrival_datetime'] = ''
        test_data[0]['departure_datetime'] = ''
        test_data[1]['arrival_datetime'] = ''
        test_data[1]['departure_datetime'] = ''
        self._generate_test_csv(test_data)
        with self.file_mock:
            calculated = Average(self.arrival, self.departure).calculate()
            self.assertEqual(calculated, '0:00:00')

    def test_check_correct_row(self):
        with self.file_mock:
            is_row_correct = Average(self.arrival,
                                     self.departure)._check_if_row_is_correct(
                Average._format_datetime('20170714T09:00:00'),
                Average._format_datetime('20170714T12:00:00')
            )
            self.assertTrue(is_row_correct)

    def test_date_formatter(self):
        dt = datetime(2017, 7, 14)
        _format_date = Average._format_datetime
        self.assertEqual(dt, _format_date(dt))

        dt_str = dt.strftime(DATETIME_FMT)
        self.assertEqual(dt, _format_date(dt_str))


if __name__ == '__main__':
    main()
