import unittest
import unittest.mock as mock

import testfile

from peewee import *
from playhouse.test_utils import test_database

test_db = SqliteDatabase(':memory:')
test_db.connect()
test_db.create_tables([testfile.Entry], safe=True)

TEST = {"name": "chris stuart",
        "task": "bowling",
        "date": "2017-03-01",
        "minutes": 30,
        "notes": "ten strikes"
        }

class LogTests(unittest.TestCase):
    @staticmethod
    def create_entries():
        testfile.Entry.create(
            name=TEST["name"],
            task=TEST["task"],
            date=TEST["date"],
            minutes=TEST["minutes"],
            notes=TEST["notes"])

    def test_get_employee(self):
        with mock.patch('builtins.input', return_value= TEST["name"]):
            assert testfile.get_name() == TEST["name"]

        with mock.patch('builtins.input', side_effect=["", "","chris"]):
            self.assertEqual(testfile.get_name(), "chris")

    def test_get_minutes(self):
        with mock.patch('builtins.input', side_effect=["one", "", 6]):
            self.assertEqual(testfile.get_minutes(), 6)

    def test_get_task(self):
        with mock.patch('builtins.input', side_effect=["", "", "eating"]):
            self.assertEqual(testfile.get_task(), "eating")

    def test_get_notes(self):
        with mock.patch('builtins.input', side_effect=["", "", "brushing teeth"]):
            self.assertEqual(testfile.get_notes(), "brushing teeth")

    def test_delete_entry(self):
        with test_database(test_db, (testfile.Entry,)):
            entry = testfile.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect=
            ["y"]):
                testfile.delete_entry(entry)
                self.assertEqual(testfile.Entry.select().count(), 0)

    def test_is_date_not_valid(self):
        date = 'asldkfjas;ldfj'
        with self.assertRaises(ValueError):
            testfile.date_validate(date)

if __name__ == "__main__":
    unittest.main()