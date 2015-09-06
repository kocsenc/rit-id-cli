import os

__author__ = 'kocsenc'

from datetime import datetime
from AttendanceAdapters.AttendanceAdapterInterface import AttendanceAdapterInterface

import logging


class FileAttendanceAdapter(AttendanceAdapterInterface):
    """
    Adapter to use if you want to save Attendance as a file

    CSV FORMAT:
    fname,lname,rit_username
    """

    def __init__(self, time_format='%m-%d-%Y %I:%M%p', extension='.txt'):
        self.filename = datetime.today().strftime(time_format) + extension

        if os.path.isfile(self.filename):
            logging.warning("Attendance filename for %s already exists! Appending." % self.filename)
        else:
            with open(self.filename, 'a') as f:
                logging.info("Created filename %s for attendance." % self.filename)

    def save(self, student_obj):
        with open(self.filename, 'a') as f:
            to_write = "%s %s,%s" % (student_obj.first_name, student_obj.last_name, student_obj.rit_id)
            f.write(to_write + '\n')
            logging.debug("Attendance file. \nWrote: %s to:\n%s" % (to_write, self.filename))
