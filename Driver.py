__author__ = "kocsenc"

from sys import argv
import re
import getpass
import hashlib

from SaveAdapters.FileAdapter import FileAdapter


def main():
    print(
        "Welcome to the RIT ID collection system. Data is encrypted with SHA-256.\n"
        "It cannot be decrypted back.\n"
        "Press 'q' to quit\n")

    adapter = FileAdapter('out.csv')
    existing_students = adapter.read_all()

    collect(FileAdapter('out.csv'))


def collect(adapter):
    raw_id = getpass.getpass("Please swipe your RIT ID.").strip()

    regex = re.compile('^;(?P<student_id>\d{9})=(?P<issue_number>\d+)\?$')

    match = re.search(regex, raw_id)
    if match:
        student_id = match.group("student_id")
        hashed_student_id = hashlib.sha256(str.encode(student_id)).hexdigest()

        issue_number = match.group("issue_number")[0]

        fname = input("First Name: ")
        lname = input("Last Name: ")
        rit_username = input("RIT username: ")

        print("hash id:\t", hashed_student_id)
        print("issue:\t\t", issue_number)
        print("Name:\t\t", fname, lname)
        print("RIT username:\t", rit_username)

        adapter.save(hashed_student_id, fname, lname, rit_username, issue_number)

    else:
        print("error")


if __name__ == "__main__":
    main()
