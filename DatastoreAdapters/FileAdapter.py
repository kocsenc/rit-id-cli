__author__ = 'kocsenc'
from DatastoreAdapters.DatastoreAdapterInterface import AdapterInterface
from Student import Student


class FileAdapter(AdapterInterface):
    """
    Adapter to use if you want to save things as a file

    CSV FORMAT:
    hashed,fname,lname,rit_username,issue_number
    """

    def __init__(self, filename):
        """
        If you wan
        :param filename:
        :return:
        """
        self.filename = filename
        self.student_dict = self.read_all()

    def save(self, hashed_sid, fname, lname, rit_username, issue_number):
        with open(self.filename, 'a') as f:
            to_write = ','.join([hashed_sid, fname, lname, rit_username, issue_number])
            f.write(to_write + '\n')

            # Save to the Student Dictionary
            self.student_dict[hashed_sid] = Student(hashed_sid, fname, lname, rit_username, issue_number)

    def read_all(self):
        students_dict = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f.readlines():
                    line = line.strip().split(',')

                    student_object = Student(line[0], line[1], line[2], line[3], line[4])
                    students_dict[line[0]] = student_object

            self.student_dict = students_dict
            return students_dict
        except IOError:
            return {}

    def read_one(self, hashed_sid):
        try:
            return self.read_all()[hashed_sid]
        except KeyError:
            return None
