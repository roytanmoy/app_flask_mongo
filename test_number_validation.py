import unittest
from processInput import processUserInput

class testvalidatePhoneNumberTest(unittest.TestCase):

    def setUp(self):
        self.data = './test.csv'
        self.ph_obj = processUserInput(self.data)
        self.raw_data = self.ph_obj.read_from_CSV_File()

    def test_csv_header_parsing(self):
        self.assertEqual(
            self.raw_data[0],
            ['id','sms_phone']
            )


if __name__ == '__main__':
    unittest.main()