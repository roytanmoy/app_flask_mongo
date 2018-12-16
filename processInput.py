import csv
import os
from validation import validatePhoneNumber as vpn

ip_file = "input_data.csv"
op_file = "output_file.csv"

COUNTRY_CODE = 'ZA'

class processUserInput():
    def __init__(self, input_file=ip_file, process_data=False, storage_type='file'):
        self.input_file = input_file
        self.process_data = process_data
        self.storage_type=storage_type
        self.fields = []
        self.vpn = vpn(COUNTRY_CODE)

    def read_from_CSV_File(self):
        rows = []
        with open(self.input_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            #self.fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
            self.fields = rows[0]
        if self.process_data:
            return self.process_Raw_Data(rows)
        else:
            return rows

    def process_Raw_Data(self, raw_data):
        resp = self.vpn.validate_numbers(raw_data)
        if self.storage_type == 'file':
            file_names = []
            path = os.path.split(self.input_file)[0]

            for fname in resp.keys():
                if resp[fname]:
                    op_file = os.path.join(path, fname+'.csv')
                    file_names.append({fname:op_file})
                    op_data = resp[fname]
                    self.fields = op_data[0].keys()
                    self.write_to_CSV_File(op_data, output_file = op_file)
            return file_names
        else:
            return resp

    def write_to_CSV_File(self, output_data, output_file = op_file):
        with open(output_file, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, self.fields)
            csvwriter.writeheader()
            csvwriter.writerows(output_data)

if __name__ == "__main__":
    ph_obj = processUserInput(ip_file)
    raw_data = ph_obj.read_from_CSV_File()
    ph_obj.process_Raw_Data(raw_data)


