from validation import validatePhoneNumber as vpn
import csv
input_file = "input_data.csv"
output_file = "final.csv"
COUNTRY_CODE = 'ZA'

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
            self.fields = self.rows[0]
        return self.rows

    def process_Raw_Data(self, raw_data):
        resp = self.vpn.validate_numbers(raw_data)

        for num_type in resp.keys():
            if resp[num_type]:
                op_file = num_type+'.csv'
                op_data = resp[num_type]
                self.fields = op_data[0].keys()
                self.write_to_CSV_File(op_data, op_file = op_file)

    def write_to_CSV_File(self, op_data, op_file = output_file):
        with open(op_file, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, self.fields)
            csvwriter.writeheader()
            csvwriter.writerows(op_data)

if __name__ == "__main__":
    ph_obj = processPhoneNumber()
    raw_data = ph_obj.read_from_CSV_File()
    ph_obj.process_Raw_Data(raw_data)
    #print (ph_obj.read_from_CSV_File(output_file))

