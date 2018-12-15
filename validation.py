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
            res = self.validate_mobile_entry(row)
            if res['result'] and not res['e164_num']:
                rowDict = {fields[0]: row[0], fields[1]: row[1], 'status':  'number is accpeted'}
                val_num.append(rowDict)
            elif res['result']:
                rowDict = {fields[0]: row[0], fields[1]: row[1], 'modified to': res['e164_num']}
                mod_num.append(rowDict)
            else:
                rowDict = {fields[0]: row[0], fields[1]: row[1], 'error message': res['msg']}
                inval_num.append(rowDict)
        return {'valid_numbers':val_num, 'invalid_numbers':inval_num, 'corrected_numbers':mod_num}

    def validate_mobile_entry(self, row):
        #number_list = re.split(NUMBER_SPLIT_REGEX, row.strip())
        number = row[1]
        return self.validate_number(number)

    def validate_number(self, number):
        msg = "exception in validating number {}".format(number)
        resp = {'number': number, 'result': False, 'e164_num': None, "msg": msg}
        if number == '':
            resp['msg'] = "empty value"
            return resp
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
                e164_num = pn.format_number(number_obj, pn.PhoneNumberFormat.E164)[1:]
                if not e164_num:
                    msg = 'number {} could not be converted to E.164.'.format(number)
                    log.error(msg)
                else:
                    resp['result'] = True
                    if number == e164_num:
                        msg = 'number {} is valid'.format(number)
                    else:
                        msg = 'number {} is corrected'.format(number)
                        resp['e164_num'] = e164_num
                    print(msg)

        except pn.NumberParseException as e:
            msg = '{}: {}'.format(e.args[0], number)
            log.error(msg)
        resp['msg'] = msg
        return resp

if __name__ == "__main__":
    ph_obj = validatePhoneNumber()
    print(ph_obj.validate_numbers([['id','number'],['1234', '+27717278645']]))