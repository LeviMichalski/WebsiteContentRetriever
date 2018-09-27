# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# file_io_tests.py
#
# Tests the file_io.py functions
#
# Follows the standard Python unittest module for creating a unit test by extending
# the unittest.TestCase class and using the self.assertXYZ functions.
#
# Authors: Levi Michalski, Tim Michalski
# License: Apache 2.0
# GitHub: https://github.com/LeviMichalski/WebsiteContentRetriever
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import unittest
from app import file_io


class FileIOTests(unittest.TestCase):

    def test_get_csv_processes_data(self):
        csv_file = file_io.get_csv('../sample-content/demo-content.csv')
        self.assertIsNotNone(csv_file)

    def test_get_csv_has_valid_records(self):
        csv_file = file_io.get_csv('../sample-content/demo-content.csv')
        self.assertEqual(
            csv_file[0][1],
            'Contractors expect more change in next 5 years than past 50'
        )
        self.assertEqual(
            csv_file[0][2],
            'https://www.constructiondive.com/news/contractors-expect-more-change-in-next-5-years-than-past-50/530454/'
        )


if __name__ == '__main__':
    unittest.main()
