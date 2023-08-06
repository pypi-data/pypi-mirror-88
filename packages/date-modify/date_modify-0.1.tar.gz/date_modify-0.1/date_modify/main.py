import unittest
import datetime
from date_modify import DateModify


class TestDateModify(unittest.TestCase):
    def setUp(self):
        super(TestDateModify, self).setUp()
        d = datetime.datetime(year=2020, month=1, day=1)
        self.dm = DateModify(d)

    def test_yesterday(self):
        self.assertEqual(self.dm.modify("yesterday").isoformat(), '2019-12-31T00:00:00')

    def test_yesterday_noon(self):
        self.assertEqual(self.dm.modify("yesterday noon").isoformat(), '2019-12-31T12:00:00')

    def test_yesterday_time(self):
        self.assertEqual(self.dm.modify("yesterday 14:00").isoformat(), '2019-12-31T14:00:00')

    def test_midnight(self):
        self.assertEqual(self.dm.modify("midnight").isoformat(), '2020-01-01T00:00:00')

    def test_today(self):
        self.assertEqual(self.dm.modify("today").isoformat(), '2020-01-01T00:00:00')

    def test_noon(self):
        self.assertEqual(self.dm.modify("noon").isoformat(), '2020-01-01T12:00:00')

    def test_tomorrow(self):
        self.assertEqual(self.dm.modify("tomorrow").isoformat(), '2020-01-02T00:00:00')

    def test_next_dayname(self):
        self.assertEqual(self.dm.modify("next thursday").isoformat(), '2020-01-02T00:00:00')

    def test_next_dayname_more(self):
        self.assertEqual(self.dm.modify("next thursday +15 hours").isoformat(), '2020-01-02T15:00:00')

    def test_last_dayname(self):
        self.assertEqual(self.dm.modify("last friday").isoformat(), '2019-12-27T00:00:00')

    def test_last_dayname_more(self):
        self.assertEqual(self.dm.modify("last saturday -2 hours").isoformat(), '2019-12-27T22:00:00')

    def test_weekday(self):
        self.assertEqual(self.dm.modify("sunday").isoformat(), '2020-01-05T00:00:00')
        self.assertEqual(self.dm.modify("sun").isoformat(), '2020-01-05T00:00:00')
        self.assertEqual(self.dm.modify("Monday").isoformat(), '2020-01-06T00:00:00')
        self.assertEqual(self.dm.modify("mon").isoformat(), '2020-01-06T00:00:00')
        self.assertEqual(self.dm.modify("tuesday").isoformat(), '2020-01-07T00:00:00')
        self.assertEqual(self.dm.modify("tue").isoformat(), '2020-01-07T00:00:00')
        self.assertEqual(self.dm.modify("wednesday").isoformat(), '2020-01-08T00:00:00')
        self.assertEqual(self.dm.modify("wed").isoformat(), '2020-01-08T00:00:00')
        self.assertEqual(self.dm.modify("thursday").isoformat(), '2020-01-02T00:00:00')
        self.assertEqual(self.dm.modify("thu").isoformat(), '2020-01-02T00:00:00')
        self.assertEqual(self.dm.modify("friday").isoformat(), '2020-01-03T00:00:00')
        self.assertEqual(self.dm.modify("fri").isoformat(), '2020-01-03T00:00:00')
        self.assertEqual(self.dm.modify("saturday").isoformat(), '2020-01-04T00:00:00')
        self.assertEqual(self.dm.modify("sat").isoformat(), '2020-01-04T00:00:00')

    def test_ago(self):
        self.assertEqual(self.dm.modify("2 days ago").isoformat(), '2019-12-30T00:00:00')
        self.assertEqual(self.dm.modify("8 days ago 14:00").isoformat(), '2019-12-23T10:00:00')
        self.assertEqual(self.dm.modify("2 months 5 days ago").isoformat(), '2019-10-27T00:00:00')
        self.assertEqual(self.dm.modify("2 months ago 5 days").isoformat(), '2019-10-27T00:00:00')

    def test_reltext_week(self):
        self.assertEqual(self.dm.modify("Tuesday last week").isoformat(), '2019-12-31T00:00:00')
        self.assertEqual(self.dm.modify("Friday last week").isoformat(), '2019-12-27T00:00:00')
        self.assertEqual(self.dm.modify("Monday next week").isoformat(), '2020-01-06T00:00:00')
        self.assertEqual(self.dm.modify("wednesday next week").isoformat(), '2020-01-08T00:00:00')
        # self.assertEqual(self.dm.modify("wednesday this week").isoformat(), '2020-01-01T00:00:00')
        # self.assertEqual(self.dm.modify("fri this week").isoformat(), '2020-01-03T00:00:00')


if __name__ == '__main__':
    unittest.main()
