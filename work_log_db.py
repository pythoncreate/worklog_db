"""
Worklog with Database Project for TreeHouse Python Course

Create a command line application that will allow employees to
enter their name, time worked, task worked on, and general notes
about the task into a database.

There should be a way to add a new entry, list all entries for
a particular employee, and list all entries that match a date
or search term.

Print a report of this information to the screen, including the date,
title of task, time spent, employee, and general notes.

Created --2017 by Chris Stuart
"""
from collections import OrderedDict
import datetime
import os

from peewee import *

db = SqliteDatabase('log.db')

fmt = '%Y-%m-%d'


class Entry(Model):
    notes = TextField()
    name = TextField()
    task = TextField()
    minutes = IntegerField()
    date = DateField(default=datetime.date.today())

    class Meta:
        database = db


def initialize():
    """Create database and table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry"""
    print("Enter your name or 'm' to return to main menu.")
    while True:
        name = input('> ')
        if name.lower().strip() != 'm':
            task = input("What task did you do? ")
            minutes = input("How many minutes did it take? ")
            notes = input("Please enter any notes about the task: ")
            date = datetime.date.today().strftime(fmt)
            Entry.create(name=name, task=task, minutes=minutes, notes=notes, date=date)
            input("Hit Enter/Return to go back and add a task or view previous entries.")
            break
        else:
            menu_loop()


def view_entries(search_employee=None, search_date=None, search_time=None, search_term=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.date.desc())

    if search_employee:
        entries = entries.where(Entry.name.contains(search_employee))

    elif search_date:
        while True:
            try:
                dt = datetime.datetime.strptime(search_date, fmt).date()
                entries = entries.where(Entry.date == dt)
                break

            except ValueError:
                print("\n\n\n")
                print("Sorry that is not a valid date format")
                search_by_date()

            else:
                print("Sorry that's not a match try again")
                search_by_date()

    elif search_time:
        entries = entries.where(Entry.minutes == int(search_time))

    elif search_term:
        entries = entries.where((Entry.task.contains(search_term))|(Entry.notes.contains(search_term)))

    for entry in entries:
        clear()
        print("Name: " + entry.name)
        print("Task: " + entry.task)
        print("Minutes Taken: " + str(entry.minutes))
        print("Task Notes: " + entry.notes)
        print("Date: " + str(entry.date))
        print('\n\n'+'='*len(entry.name))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_by_employee():
    view_entries(search_employee=input('Search query: '))


def search_by_date():
    view_entries(search_date=input('Enter Date in Format(yyyy-mm-dd)): '))


def search_by_time():
    view_entries(search_time=input('Enter a number of minutes (whole number only): '))
    # while True:
    #     search_time = (input('Search query: '))
    #     try:
    #         search_time = int(search_time)
    #         view_entries(search_time)
    #     except ValueError:
    #         print("Not a valid entry. Please try again")


def search_by_term():
    view_entries(search_term = input('Search query: '))


def search_entries():
    """Search previous entries"""
    # view_entries(input('Search query: '))
    while True:
        lookup = input("Lookup by Employee(E), Date(D), Time(T) or Search Term(S): ")
        lookup.lower()

        if lookup == 'e':
            search_by_employee()
            break
        elif lookup == 'd':
            search_by_date()
            break
        elif lookup == 't':
            search_by_time()
            break
        elif lookup == 's':
            search_by_term()
            break
        else:
            print("Sorry invalid option. Please try again")


def delete_entry(entry):
    """Delete an entry"""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry Deleted")

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()