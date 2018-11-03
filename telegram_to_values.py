import sys
import serial
import re

list_of_interesting_codes = {
    '1-0:1.8.1': 'total_received_1',
    '1-0:1.8.2': 'total_received_2',
    '1-0:2.8.1': 'total_deliverd_1',
    '1-0:2.8.2': 'total_deliverd_2',
}

pattern = re.compile(b'\r\n(?=!)')

good_checksum = False


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
    ser = port_config()

    try:
        ser.open()
    except:
        sys.exit("Fout bij het openen van %s. Aaaaarch." % ser.name)

    checksum_found = False
    tel = b''
    while not checksum_found:
        # Read in a line
        tel_line = ser.readline()

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
print(telegram)

telegram_values = dict()
for telegram_line in telegram.split(b'\r\n'):
    # Split the OBIS code from the value
    # The lines with a OBIS code start with a number
    if re.match(b'\d', telegram_line):
        code = b''.join(re.split(b'(\()', telegram_line)[:1])
        value = b''.join(re.split(b'(\()', telegram_line)[1:])
        telegram_values[code] = value

#nicely print codes and convert to strings
for code, value in telegram_values.items():
    code_string = code.decode('utf-8').strip()
    if code_string in list_of_interesting_codes:
        # Cleanup value
        clean_value = float(value.lstrip(b'\(').rstrip(b'\)*kWhA'))
        # Print nicely formatted string

        print(code_string, ': ', list_of_interesting_codes[code_string], ' - ', clean_value)

