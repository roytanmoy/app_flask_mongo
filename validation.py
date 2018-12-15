import re
import logging as log
import phonenumbers as pn
NUMBER_SPLIT_REGEX = u'[;,]*'

class validatePhoneNumber():
    def __init__(self, countryCode="ZA"):
        self.countryCode = countryCode
        self.valid_numbers = []
        self.modified_numbers = []
        self.invalid_numbers = []

    def validate_numbers(self, raw_data):
        fields = raw_data.pop(0)
        val_num = []
        inval_num = []
        mod_num = []
        for row in raw_data:
            rowDict = {fields[0]: row[0], fields[1]: row[1]}
            resp = self.validate_mobile_entry(row)
            if resp['result'] and not resp['e164_number']:
                val_num.append(rowDict)
            elif resp['result'] and resp['e164_number']:
                mod_num.append(rowDict)
            else:
                inval_num.append(rowDict)
        return {'val_num':val_num, 'inval_num':inval_num, 'mod_num':mod_num}

    def validate_mobile_entry(self, row):
        #number_list = re.split(NUMBER_SPLIT_REGEX, row.strip())
        number = row[1]
        if number == '':
            return {'number':number, 'result':False, 'e164_number': None, "msg":"no value"}
        else:
            return self.validate_number(number)

    def validate_number(self, number):
        result = False
        e164_num = None
        msg = "exception in validating number {}".format(number)
        resp = {'number': number, 'result': result, 'e164_number': e164_num, "msg": msg}
        try:
            if number.startswith('+'):
                number_obj = pn.parse(number)
            else:
                number_obj = pn.parse(number, self.countryCode)

            if not pn.is_possible_number(number_obj):
                msg = 'Number is not possibly valid: {}.'.format(number)
                log.error(msg)
            elif not pn.is_valid_number(number_obj):
                msg = 'Number is not valid: {}.'.format(number)
                log.error(msg)
            else:
                e164_num = pn.format_number(number_obj, pn.PhoneNumberFormat.E164)
                if not e164_num:
                    msg = 'number {} could not be converted to E.164.'.format(number)
                    log.error(msg)
                else:
                    msg = 'number {} is valid'.format(number)
                    print(msg)
                    resp['result'] = True
                    resp['e164_num'] = e164_num

        except pn.NumberParseException as e:
            msg = '{}: {}'.format(e.args[0], number)
            log.error(msg)
        resp['msg'] = msg
        return resp

if __name__ == "__main__":
    ph_obj = validatePhoneNumber()
    #print(ph_obj.validate_number("2.63717E+11"))
    print(ph_obj.validate_numbers([['id','number'],['1234', '2.63717E+11']]))