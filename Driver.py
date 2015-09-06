__author__ = "kocsenc"

import re
import getpass
import hashlib

from DatastoreAdapters.FileDatastoreAdapter import FileDatastoreAdapter
from AttendanceAdapters.FileAttendanceAdapter import FileAttendanceAdapter


def main():
    print(
        "Welcome to the RIT ID check-in system. Data is safe & encrypted with SHA-256."
        "It cannot be decrypted back.\n"
        "Press 'q' to quit\n")

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

    # print("Name:\t\t", fname, lname)
    # print("RIT username:\t", rit_username)
    return fname, lname, rit_username


def validate_username(raw_username):
    regex = re.compile('(\w{2,3}\d{4})')
    match = re.search(regex, raw_username)

    username = ""
    if match:
        username = match.group(0)

    return username


def check_in(student):
    """
    Creates a separate output file with the attendance of the children.
    :param student: Student Object
    """
    # TODO: Perform check in action
    print("Thanks, %s. You are checked in! \t=====>\n\n" % student.first_name)


if __name__ == "__main__":
    main()
