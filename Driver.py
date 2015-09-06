__author__ = "kocsenc"

import re
import getpass
import hashlib
import logging

from DatastoreAdapters.FileDatastoreAdapter import FileDatastoreAdapter
from AttendanceAdapters.FileAttendanceAdapter import FileAttendanceAdapter


def main():
    print(
        """
     (~)
      K
     _C_
  .-'-.-'-.
 /        \\
|   .-------'._
|  / /  '.' '.\\
|  \ \ @   @ / /
|   '---------'
|    _______|
|  .'-+-+-+|
|  '.-+-+-+|     Welcome to the RIT ID check-in system.
|           |    Data is safe & encrypted with SHA-256, so no one can read it.
'-.______.-'    Press 'q' to quit
        """
    )

    # Set logging preferences (mostly for developers only)
    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.WARNING)

    # Setup your data store (storage) and attendance adapters.

    data_source = FileDatastoreAdapter('db.csv')
    attendance_adapter = FileAttendanceAdapter()

    while True:
        try:
            collect(data_source, attendance_adapter, take_attendance=True)
        except KeyboardInterrupt:
            print("Closing, thanks!")
            break


def collect(data_source, attendance_adapter, take_attendance=True):
    raw_id = getpass.getpass("Please swipe your RIT ID").strip()
    if raw_id.lower() == 'q' or raw_id.lower() == 'quit':
        raise KeyboardInterrupt

    regex = re.compile('^;(?P<student_id>\d{9})=(?P<issue_number>\d+)\?$')
    match = re.search(regex, raw_id)

    if match:
        student_id = match.group("student_id")
        hashed_student_id = hashlib.sha256(str.encode(student_id)).hexdigest()
        issue_number = match.group("issue_number")[0]

        # If the student wasn't registered before, register them
        if hashed_student_id not in data_source.student_dict:
            (fname, lname, rit_username) = register()
            data_source.save(hashed_student_id, fname, lname, rit_username, issue_number)

        # At this point we can guarantee that a student object is ready for use.
        student = data_source.student_dict[hashed_student_id]

        if take_attendance:
            check_in(attendance_adapter, student)

    else:
        print("Are you sure you swiped your RIT id? Try again.")


def register():
    """
    Is in charged of registering a new user. Prompts the user then returns the data.
    :return: first_name, last_name, rit username
    """
    print("Welcome, since it is your first time, we need some more info.")

    fname = input("First Name: ")
    lname = input("Last Name: ")
    rit_username = validate_username(input("RIT username: "))

    logging.debug("Name:\t\t", fname, lname)
    logging.debug("RIT username:\t", rit_username)
    return fname, lname, rit_username


def validate_username(raw_username):
    regex = re.compile('(\w{2,3}\d{4})')
    match = re.search(regex, raw_username)

    username = ""
    if match:
        username = match.group(0)

    return username


def check_in(adapter, student):
    """
    Creates a separate output file with the attendance of the children.
    :param adapter: The Attendance Adapter
    :param student: The student object
    :return:
    """
    adapter.save(student)
    print(mr_poo_message(top="Thanks, %s!" % student.first_name, bottom="You are checked in!"))


def mr_poo_message(message="Woot", top=None, bottom=None):
    offset = 32
    p1 = top or message[:offset]
    p2 = bottom or message[offset:]
    poo = """
    ,~~~~~~,
   / ,     \\
  /,~|_______\.
 /~ (__________)
(*)  ; (^)(^)':
    =;  ____  ;
      ; ''''  ;=
{"}_   ' '""' ' _{"}    `~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
\__/     >  <   \__/   `'  %s
  \    ,"   ",  /       |  %s
   \  "       /"        ',____________________________________,"
      "      "=
       >     <
      -`.   ,'
      `--'\n
""" % (p1, p2)
    return poo


if __name__ == "__main__":
    main()
