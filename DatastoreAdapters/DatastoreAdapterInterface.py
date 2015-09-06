__author__ = 'kocsenc'


class DatastoreAdapterInterface:
    def save(self, hashed_sid, fname, lname, rit_username, issue_number):
        raise NotImplementedError()

    def read_all(self):
        """
        Must return a dictionary where
        key: hashed student id
        value: Student object (contains all student data)

        :return:
        """
        raise NotImplementedError()

    def read_one(self, hashed_sid):
        """
        Return a student object given the hashed_sid, or NONE if not found

        :param hashed_sid: Hashed student it
        :return:
        """
        raise NotImplementedError()
