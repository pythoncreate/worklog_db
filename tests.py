import unittest

from peewee import *

import work_log_db

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([work_log_db.Entry], safe=True)

TEST_DATA = {
    'name': 'chris stuart',
    'task': 'gardening',
    'minutes': '30',
    'date': '2017/02/2016',
    'notes': 'planted roses'
}


class LogTests(unittest.TestCase):

    def setUp(self):
        self.Entry = work_log_db.view_entries(TEST_DATA)

    def find_employee(self):
        self.assertTrue(TEST_DATA['name'], 'chris stuart')

    def test_equal_minutes(self):
        minutes = 30
        search_time = 30
        self.assertEqual(minutes, search_time)

    def test_minutes_not_equal(self):
        minutes = 30
        search_time = 45
        self.assertNotEqual(minutes,search_time)

    def test_equal_date(self):
        date = '2017/04/02'
        search_date = '2017/04/02'
        self.assertEqual(date,search_date)

    def test_date_not_equal(self):
        date = '2017/04/02'
        search_date = '2017/04/01'
        self.assertNotEqual(date,search_date)

    def test_name_equal(self):
        name = 'chris stuart'
        search_employee = 'chris stuart'
        self.assertEqual(name,search_employee)

    def test_name_not_equal(self):
        name = 'chris stuart'
        search_employee = 'ted jones'
        self.assertNotEqual(name,search_employee)

    def test_menu(self):
        choice = 'q'
        self.assertEqual(choice,'q')

class EntryTests(unittest.TestCase):
    def setUp(self):
        self.entry1 = work_log_db.Entry(name='chris', minutes='30', task='garden', date='lkjlkhlj')
        self.entry2 = work_log_db.Entry(name='joe', minutes='20', task='bowling', date='2017-03-02')

    def test_creation(self):
        self.assertEqual(self.entry1.name, 'chris')
        self.assertIn(self.entry1.task, 'gardening')
        self.assertIsInstance(self.entry2.minutes, str)

    # def test_bad_description(self):
    #     self.assertRaises(ValueError, work_log_db.view_entries(search_date="alksjfdlskajfd"))


if __name__ == '__main__':
    unittest.main()