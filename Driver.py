__author__ = "kocsenc"

import re
import getpass
import hashlib
import logging

from DatastoreAdapters.FileDatastoreAdapter import FileDatastoreAdapter
from AttendanceAdapters.FileAttendanceAdapter import FileAttendanceAdapter


class Driver:
    """
    The main Driver class for the system. In charge of kicking everything off
    """

    def __init__(self, data_source=None, attendance_adapter=None, take_attendance=True):
        self.print_welcome_message()

        # Set logging preferences (mostly for developers only)
        logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.WARNING)

        # Setup your data store (storage) and attendance adapters.
        self.data_source = data_source or FileDatastoreAdapter('db.csv')
        self.attendance_adapter = attendance_adapter or FileAttendanceAdapter()
        self.take_attendance = take_attendance

        self.attendance_buffer = {}

    def run(self):
        while True:
            try:
                self._collect(take_attendance=self.take_attendance)
            except KeyboardInterrupt:
                print("Closing, thanks!")
                break

    def _collect(self, take_attendance=True):
        raw_id = getpass.getpass("Please swipe your RIT ID").strip()

        if raw_id.lower() == 'q' or raw_id.lower() == 'quit':
            raise KeyboardInterrupt

        regex = re.compile('^;(?P<student_id>\d{9})=(?P<issue_number>\d+)\?$')
        match = re.search(regex, raw_id)

        if match:
            student_id = match.group("student_id")
            hashed_student_id = hashlib.sha512(str.encode(student_id)).hexdigest()
            issue_number = match.group("issue_number")[0]

            # If the student wasn't registered before, register them
            if hashed_student_id not in self.data_source.student_dict:
                (fname, lname, rit_username) = self._register()
                self.data_source.save(hashed_student_id, fname, lname, rit_username, issue_number)

            # At this point we can guarantee that a student object is ready for use.
            student = self.data_source.student_dict[hashed_student_id]

            if take_attendance:
                if student.hashed_sid not in self.attendance_buffer:
                    self.check_in(student)
                    self.attendance_buffer[student.hashed_sid] = student
                else:
                    print(mr_poo_message(top="Oh my, %s!" % student.first_name, bottom="You already have checked in!"))

            else:
                print("Are you sure you swiped your RIT id? Try again.")

    def check_in(self, student):
        """
        Creates a separate output file with the attendance of the children.
        :param adapter: The Attendance Adapter
        :param student: The student object
        :return:
        """
        self.attendance_adapter.save(student)
        print(mr_poo_message(top="Thanks, %s!" % student.first_name, bottom="You are checked in!"))

    @staticmethod
    def _register():
        """
        Prompts the user for registration data, then returns the data.
        :return: (first_name, last_name, rit username)
        """
        print("Welcome, since it is your first time, we need some more info.")

        fname = input("First Name: ")
        lname = input("Last Name: ")
        rit_username = Driver._validate_username(input("RIT username: "))

        logging.debug("Name:\t\t", fname, lname)
        logging.debug("RIT username:\t", rit_username)
        return fname, lname, rit_username

    @staticmethod
    def _validate_username(raw_username):
        regex = re.compile('(\w{2,3}\d{4})')
        match = re.search(regex, raw_username)

        username = ""
        if match:
            username = match.group(0)

        return username

    @staticmethod
    def print_welcome_message():
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
|    _______|    = Welcome to the RIT ID check-in system. =
|  .'-+-+-+|
|  '.-+-+-+|     Data is safe & encrypted with SHA-512, so no one can read it.
|           |    That means it is not solvable in asymptotic polynomial time.
'-.______.-'   ** Press 'q' to quit
            """
        )


def main():
    d = Driver()
    d.run()


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
      `--'

""" % (p1, p2)
    return poo


if __name__ == "__main__":
    main()
