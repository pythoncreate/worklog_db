import unittest
import unittest.mock as mock

import worklog

from peewee import *
from playhouse.test_utils import test_database

test_db = SqliteDatabase(':memory:')
test_db.connect()
test_db.create_tables([worklog.Entry], safe=True)

TEST = {"name": "chris stuart",
        "task": "bowling",
        "date": "2017",
        "minutes": 30,
        "notes": "ten strikes"
        }

class LogTests(unittest.TestCase):
    @staticmethod
    def create_entries():
        worklog.Entry.create(
            name=TEST["name"],
            task=TEST["task"],
            date=TEST["date"],
            minutes=TEST["minutes"],
            notes=TEST["notes"])

    def test_get_employee(self):
        with mock.patch('builtins.input', return_value= TEST["name"]):
            assert worklog.get_name() == TEST["name"]

        with mock.patch('builtins.input', side_effect=["", "","chris"]):
            self.assertEqual(worklog.get_name(), "chris")

    def test_get_minutes(self):
        with mock.patch('builtins.input', side_effect=["one", "", 6]):
            self.assertEqual(worklog.get_minutes(), 6)

    def test_date_validate(self):
        search_date = ""
        self.assertFalse(worklog.date_validate(search_date))

    def test_time_validate(self):
        search_time = "badstring"
        self.assertFalse(worklog.time_validate(search_time))

    def test_get_task(self):
        with mock.patch('builtins.input', side_effect=["", "", "eating"]):
            self.assertEqual(worklog.get_task(), "eating")

    def test_get_notes(self):
        with mock.patch('builtins.input', side_effect=["", "", "brushing teeth"]):
            self.assertEqual(worklog.get_notes(), "brushing teeth")

    def test_delete_entry(self):
        with test_database(test_db, (worklog.Entry,)):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect=
            ["y"]):
                worklog.delete_entry(entry)
                self.assertEqual(worklog.Entry.select().count(), 0)

    def test_search_menu(self):
        search = None
        with mock.patch('builtins.input', side_effect=
            ["e", "d", "t", "s"]):
            self.assertEqual(worklog.search_entries(), search)

if __name__ == "__main__":
    unittest.main()