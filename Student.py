__author__ = 'kocsenc'

class Student:
    def __init__(self, hashed_sid, fname, lname, rit_id, issue_num):
        self.hashed_sid = hashed_sid
        self.first_name = fname
        self.last_name = lname
        self.rit_id = rit_id
        self.issue_number = issue_num
