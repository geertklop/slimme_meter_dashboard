import sys
import serial
import re


def port_config():
#Set COM port config
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.bytesize=serial.EIGHTBITS
    ser.parity=serial.PARITY_NONE
    ser.stopbits=serial.STOPBITS_ONE
    ser.xonxoff=0
    ser.rtscts=0
    ser.timeout=20
    ser.port="/dev/ttyUSB0"

    return ser


def read_telegram():
    """
    Opens serial port and adds lines until checksum is found
    :return: raw telegram
    """
    ser = port_config()

    try:
        ser.open()
    except:
        sys.exit("Fout bij het openen van {}".format(ser.name))

    checksum_found = False
    tel = b''
    while not checksum_found:
        # Read in a line
        tel_line = ser.readline()
        print(tel_line)

        # End of telegram found or not
        if re.match(b'(?=!)', tel_line):
            # print('')
            tel = tel + tel_line
            checksum_found = True
        else:
            tel = tel + tel_line

    ser.close()

    return tel


telegram = read_telegram()

def telegram_to_dict(telegram_raw):
    """
    Splits raw telegram into raw dictionary
    :param telegram_raw: telegram from read_telegram()
    :return: dictionary of telegram
    """
    telegram_values = dict()
    for telegram_line in telegram_raw.split(b'\r\n'):
        # Split the OBIS code from the value
        # The lines with a OBIS code start with a number
        if re.match(b'\d', telegram_line):
            code = b''.join(re.split(b'(\()', telegram_line)[:1])
            value = b''.join(re.split(b'(\()', telegram_line)[1:])
            telegram_values[code] = value

    return telegram_values


#nicely print codes and convert to strings
def extract_interesting_codes(telegram_dict, codes = list_of_interesting_codes):
    """
    Extract interesting values from telegram_dict and convert to numbers
    :param telegram_dict: dict of telegram
    :param codes: dict of interesting codes
    :return: dict of intersting values
    """
    clean_dict = dict()
    for code, value in telegram_dict.items():
        code_string = code.decode('utf-8').strip()
        if code_string in codes:
            # Cleanup value
            clean_value = float(value.lstrip(b'\(').rstrip(b'\)*kWhA'))

            # add to dict
            clean_dict[code_string] = clean_value

    return clean_dict



