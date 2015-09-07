import logging

__author__ = 'kocsenc'

import sqlite3

from Student import Student
from DatastoreAdapters.DatastoreAdapterInterface import DatastoreAdapterInterface


class SqliteAdapter(DatastoreAdapterInterface):
    def __init__(self, dbname='db.sqlite'):
        self.conn = sqlite3.connect(dbname)

        self.TABLE = "students"

        self.SID_COL = "sid"
        self.FNAME_COL = "fname"
        self.LNAME_COL = "lname"
        self.USERNAME_COL = "rit_username"
        self.ISSUE_COL = "issue_number"

        # Check if the table/db has been set, if not set it
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS students (sid text primary key, fname text, lname text, rit_username text, issue_number integer);")
        self.conn.commit()

        self.student_dict = self.read_all()

    def save(self, hashed_sid, fname, lname, rit_username, issue_number):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?);",
            (hashed_sid, fname, lname, rit_username, issue_number)
        )
        self.conn.commit()
        self.student_dict[hashed_sid] = Student(hashed_sid, fname, lname, rit_username, issue_number)

    def read_all(self):
        c = self.conn.cursor()

        query = "SELECT sid, fname, lname, rit_username, issue_number from students;"
        students = c.execute(query)

        student_dict = {}
        for student in students:
            student_dict[student[0]] = Student(student[0], student[1], student[2], student[3], student[4])

        return student_dict

    def read_one(self, hashed_sid):
        if self.student_dict[hashed_sid]:
            return self.student_dict[hashed_sid]

        c = self.conn.cursor()
        c.execute("SELECT sid, fname, lname, rit_username, issue_number FROM students WHERE sid=?", hashed_sid)

        fetched_student = c.fetchone()
        if fetched_student:
            hashed_sid = fetched_student[0]
            self.student_dict[hashed_sid] = Student(hashed_sid, fetched_student[1], fetched_student[2],
                                                    fetched_student[3], fetched_student[4])
            return self.student_dict[hashed_sid]
        else:
            return None

    def __del__(self):
        try:
            self.conn.close()
        except:
            logging.error("Couldnt appropriately close connection to SQLITE db")
