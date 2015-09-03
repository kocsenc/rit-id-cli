__author__ = "kocsenc"

import re
import getpass
import hashlib

from SaveAdapters.FileAdapter import FileAdapter


def main():
    print(
        "Welcome to the RIT ID check-in system. Data is encrypted with SHA-256.\n"
        "It cannot be decrypted back.\n"
        "Press 'q' to quit\n")

    adapter = FileAdapter('out.csv')

    while True:
        try:
            collect(adapter)
        except KeyboardInterrupt:
            print("Closing, thanks!")


def collect(adapter):
    raw_id = getpass.getpass("Please swipe your RIT ID").strip()
    regex = re.compile('^;(?P<student_id>\d{9})=(?P<issue_number>\d+)\?$')
    match = re.search(regex, raw_id)

    if match:
        student_id = match.group("student_id")
        hashed_student_id = hashlib.sha256(str.encode(student_id)).hexdigest()
        issue_number = match.group("issue_number")[0]

        if hashed_student_id not in adapter.student_dict:
            print("Welcome, since it is your first time, we need some more info.")

            fname = input("First Name: ")
            lname = input("Last Name: ")
            rit_username = validate_username(input("RIT username: "))

            # print("Name:\t\t", fname, lname)
            # print("RIT username:\t", rit_username)

            adapter.save(hashed_student_id, fname, lname, rit_username, issue_number)

        check_in(adapter.student_dict[hashed_student_id])

    else:
        print("Are you sure you swiped your RIT id? Try again.\n")


def validate_username(raw_username):
    regex = re.compile('(\w{2,3}\d{4})')
    match = re.search(regex, raw_username)

    username = ""
    if match:
        username = match.group(0)

    return username


def check_in(student):
    # TODO: Perform check in action

    print("Thanks, %s. You are good to go! \t=====>\n\n\n\n\n" % student.first_name)


if __name__ == "__main__":
    main()
