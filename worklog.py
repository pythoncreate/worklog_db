from collections import OrderedDict
import datetime
import os

from peewee import *

db = SqliteDatabase('w.db')

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


def get_name():
    while True:
        name = input('> ')
        if name == "":
            print("Sorry nothing there. Try again")
            continue
        else:
            return name


def get_task():
    while True:
        task = input("What task did you do? ")
        if task == "":
            print("Sorry nothing there")
            continue
        else:
            return task


def get_minutes():
    while True:
        minutes = input("How many minutes did it take? ")
        if minutes == "":
            print("Sorry nothing there")
            continue
        try:
            minutes = int(minutes)
            return minutes
        except ValueError:
            print ("Sorry invalid entry")
            continue


def get_notes():
    while True:
        notes = input("Please enter any notes about the task: ")
        if notes == "":
            print("Sorry nothing there.")
            continue
        else:
            return notes

def add_entry():
    """Add an entry"""
    print("Enter your name or 'm' to return to main menu.")
    while True:
        name = get_name()
        if name.lower().strip() != 'm':
            task = get_task()
            minutes = get_minutes()
            notes = get_notes()
            Entry.create(name=name, task=task, minutes=minutes, notes=notes, date=datetime.date.today().strftime(fmt))
            input("Hit Enter/Return to go back and add a task or view previous entries.")
            break
        else:
            menu_loop()


def date_validate(search_date):
    while True:
        try:
            search_date = datetime.datetime.strptime(search_date, fmt).date()
        except (ValueError, TypeError):
            return False
        else:
            return search_date


def time_validate(search_time):
    while True:
        try:
            search_time = int(search_time)
        except ValueError:
            return False
        else:
            return search_time


def view_entries(search_employee=None, search_date=None, search_time=None, search_term=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.date.desc())

    if search_employee:
        entries = entries.where(Entry.name.contains(search_employee))
        while True:
            if not entries:
                print("Sorry No Match. Try again")
                search_by_employee()
                break
            else:
                break

    elif search_date:
        search_date = date_validate(search_date)
        entries = entries.where(Entry.date == search_date)
        while True:
            if not entries:
                print("Sorry Not a Match")
                search_by_date()
                break
            else:
                break

    elif search_time:
        search_time = time_validate(search_time)
        entries = entries.where(Entry.minutes == int(search_time))
        while True:
            if not entries:
                print("Sorry No Match. Try again")
                search_by_time()
                break
            else:
                break

    elif search_term:
        entries = entries.where((Entry.task.contains(search_term))|(Entry.notes.contains(search_term)))
        while True:
            if not entries:
                print("Sorry No Match. Try again")
                search_by_term()
                break
            else:
                break

    for entry in entries:
        clear()
        print("Name: " + entry.name)
        print("Task: " + entry.task)
        print("Minutes Taken: " + str(entry.minutes))
        print("Task Notes: " + entry.notes)
        print("Date: " + str(entry.date))
        print('\n\n' + '=' * len(entry.name))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_by_employee():
    view_entries(search_employee = input('Search By Employee Name: '))


def search_by_date():
    view_entries(search_date=input('Enter Date in Format(yyyy-mm-dd)): '))


def search_by_time():
    view_entries(search_time=input('Enter Number Minutes : '))


def search_by_term():
    view_entries(search_term = input('Search query: '))


def search_entries():
    """Search previous entries"""
    # view_entries(input('Search query: '))
    while True:
        lookup = input("Lookup by Employee(E), Date(D), Time(T) or Search Term(S): ")
        lookup.lower()

        if lookup == 'e':
            search = search_by_employee()
            return search
        elif lookup == 'd':
            search = search_by_date()
            return search
        elif lookup == 't':
            search = search_by_time()
            return search
        elif lookup == 's':
            search = search_by_term()
            return search
        elif lookup == 'm':
            menu_loop()
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