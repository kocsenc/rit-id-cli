from Student import Student

__author__ = 'kocsenc'

import sqlite3

from DatastoreAdapters.DatastoreAdapterInterface import DatastoreAdapterInterface


class SqliteAdapter(DatastoreAdapterInterface):
    def __init__(self, dbname='db.sqlite'):
        self.student_dict = self.read_all()

        self.conn = sqlite3.connect(dbname)

        self.TABLE = "students"

        self.SID_COL = "sid"
        self.FNAME_COL = "fname"
        self.LNAME_COL = ""
        self.USERNAME_COL = ""
        self.ISSUE_COL = ""

        # Check if the table/db has been set, if not set it
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS students (sid text primary key, fname text, lname text, rit_username text, issue_number integer);")
        self.conn.commit()

    def save(self, hashed_sid, fname, lname, rit_username, issue_number):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?);",
            (hashed_sid, fname, lname, rit_username, issue_number)
        )
        self.conn.commit()
        self.student_dict[hashed_sid] = Student(hashed_sid, fname, lname, rit_username, issue_number)

    def read_all(self):
        pass

    def read_one(self, hashed_sid):
        pass

    def __del__(self):
        self.conn.close()


x = SqliteAdapter()
