__author__ = 'kocsenc'


class AdapterInterface:
    def save(self, student_object):
        """
        This method is supposed to use the data within the student object to save it to whatever
        it's saving it as.
        :param student_object:
        :return:
        """
        raise NotImplementedError()
