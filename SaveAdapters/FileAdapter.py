__author__ = 'kocsenc'
from SaveAdapters.AdapterInterface import AdapterInterface
from Student import Student


class FileAdapter(AdapterInterface):
    """
    Adapter to use if you want to save things as a file

    FORMAT:
    hashed,fname,lname,rit_username,issue_number
    """

    def __init__(self, filename):
        """
        If you wan
        :param filename:
        :return:
        """
        self.student_dict = None
        self.filename = filename

    def save(self, hashed_sid, fname, lname, rit_username, issue_number):
        with open(self.filename, 'a') as f:
            to_write = ','.join([hashed_sid, fname, lname, rit_username, issue_number])
            f.write(to_write + '\n')

    def read_all(self):
        return_dict = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f.readlines():
                    line = line.strip().split(',')

                    student_object = Student(line[0], line[1], line[2], line[3], line[4])
                    return_dict[line[0]] = student_object

            self.student_dict = return_dict
            return return_dict
        except FileNotFoundError:
            return {}

    def read_one(self, hashed_sid):
        try:
            return self.read_all()[hashed_sid]
        except KeyError:
            return None
