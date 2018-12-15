import re
import logging as log
import phonenumbers as pn
NUMBER_SPLIT_REGEX = u'[;,]*'

class validatePhoneNumber():
    def __init__(self, countryCode="US"):
        self.countryCode = countryCode
        self.valid_numbers = []
        self.modified_numbers = []
        self.invalid_numbers = []

    def validate_numbers(self, raw_data):
        fields = raw_data.pop(0)
        valid_num = invalid_num = mod_num = []
        for row in raw_data:
            rowDict = {fields[0]: row[0], fields[1]: row[1]}
            resp = self.validate_mobile_entry(row)
            if resp['result'] and not resp['e164_number']:
                valid_num.append(rowDict)
            elif resp['result'] and resp['e164_number']:
                mod_num.append(rowDict)
                errorlist.append(
                    {'Row': rownum, 'Value': result['number'],
                     'Error': result['errormessage']})
            else:
                invalid_num.append(rowDict)

        return [valid_num, invalid_num, mod_num]

    def validate_mobile_entry(self, row):
        log.debug('Validating row with number field: {}'.format(row))
        #number_list = re.split(NUMBER_SPLIT_REGEX, row.strip())
        number = row[1]
        if number == '':
            return {'number':number, 'result':False, 'e164_number': None, "msg":"no value"}
        else:
            return self.validate_number(number)

    def validate_number(self, number):
        print(number)
        result = False
        e164_num = None
        if number.startswith('+'):
            number_obj = pn.parse(number)
        else:
            number_obj = pn.parse(number, self.countryCode)
        try:
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
                    print (msg)
                    result = True
        except:
            err = "exception in validating number {}".format(number)
            return {'number':number, 'result':result, 'e164_number': e164_num, "msg":err}
        return {'number':number, 'result':result, 'e164_number': e164_num, "msg":msg}

if __name__ == "__main__":
    ph_obj = validatePhoneNumber()
    print(ph_obj.validate_number("11 462 3342"))
    #ph_obj.number_to_e164("+27 11 462 3342")

