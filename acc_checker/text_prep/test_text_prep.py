import os
from text_prep2 import FileProcessor
import unittest

class TestFileProcessor(unittest.TestCase):


    def test_initiate_class(self):
        fp = FileProcessor()


    # def test_save_as_temp_file(self):   # can take file
    #     fp = FileProcessor()
    #     with open('test.pdf', 'rb') as file:
    #         fp.save_as_temp_file(file)


    def test_load_data(self):
        fp = FileProcessor()
        data = fp.load_data('test.pdf')
        assert 'Foo-bar ban-anas Py-Charm' in data.page_content


if __name__ == '__main__':
    unittest.main()