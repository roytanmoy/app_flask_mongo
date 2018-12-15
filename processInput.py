from validation import validatePhoneNumber as vpn
import csv
input_file = "aapl.csv"
output_file = "final.csv"
COUNTRY_CODE = 'ZAF'

class processPhoneNumber():
    def __init__(self):
        self.fields = []
        self.rows = []
        self.vpn = vpn(COUNTRY_CODE)

    def read_from_CSV_File(self, ip_file = input_file):
        with open(ip_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            #self.fields = next(csvreader)
            for row in csvreader:
                self.rows.append(row)
        return self.rows

    def process_Raw_Data(self, raw_data):
        self.op_data = []
        resp = self.vpn.validate_numbers(raw_data)
        valid_number= resp['valid_number']
        invalid_number = resp['invalid_number']
        modified_number = resp['modified_number']
        for i in resp:
            op_data = resp[rows]
            rowDict = {self.fields[0]: row[0], self.fields[1]: row[1]}
            self.op_data.append(rowDict)

        for row in self.rows:
            rowDict = {self.fields[0]:row[0], self.fields[1]:row[1]}
            self.op_data.append(rowDict)
        self.write_to_CSV_File()

    def write_to_CSV_File(self, op_file = output_file):
        with open(op_file, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, self.fields)
            csvwriter.writeheader()
            csvwriter.writerows(self.op_data)


if __name__ == "__main__":
    ph_obj = processPhoneNumber()
    raw_data = ph_obj.read_from_CSV_File()
    ph_obj.process_Raw_Data(raw_data)
    #ph_obj.write_to_CSV_File(op_data)
    displayData = ph_obj.read_from_CSV_File(output_file)
    print(displayData)
