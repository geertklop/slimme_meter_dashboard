# DSMR v4.2 p1 uitlezen
# (c) 10-2012 - 2016 GJ - gratis te kopieren en te plakken
versie = "1.1"
import sys
import serial
import re


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

# interesting DSMR 5 codes
list_of_interesting_codes = {
    '1-0:1.8.1': 'Meter Reading electricity delivered to client (Tariff 1) in kWh',
    '1-0:1.8.2': 'Meter Reading electricity delivered to client (Tariff 2) in kWh',
    '1-0:2.8.1': 'Meter Reading electricity delivered by dient (Tariff 1) in kWh',
    '1-0:2.8.2': 'Meter Reading electricity delivered by client (Tariff 2) in kWh',
    '0-0:96.14.0': 'Tariff indicator electricity',
    '1-0:1.7.0': 'Actual electricity power delivered (+P) in kW',
    '1-0:2.7.0': 'Actual electricity power received (-P) in kW',
    # '0-0:17.0.0': 'The actual threshold electricity in kW',
    # '0-0:96.3.10': 'Switch position electricity',
    # '0-0:96.7.21': 'Number of power failures in any phase',
    # '0-0:96.7.9': 'Number of long power failures in any phase',
    # '1-0:32.32.0': 'Number of voltage sags in phase L1',
    # '1-0:52.32.0': 'Number of voltage sags in phase L2',
    # '1-0:72:32.0': 'Number of voltage sags in phase L3',
    # '1-0:32.36.0': 'Number of voltage swells in phase L1',
    # '1-0:52.36.0': 'Number of voltage swells in phase L2',
    # '1-0:72.36.0': 'Number of voltage swells in phase L3',
    # '1-0:31.7.0': 'Instantaneous current L1 in A',
    # '1-0:51.7.0': 'Instantaneous current L2 in A',
    # '1-0:71.7.0': 'Instantaneous current L3 in A',
    # '1-0:21.7.0': 'Instantaneous active power L1 (+P) in kW',
    # '1-0:41.7.0': 'Instantaneous active power L2 (+P) in kW',
    # '1-0:61.7.0': 'Instantaneous active power L3 (+P) in kW',
    # '1-0:22.7.0': 'Instantaneous active power L1 (-P) in kW',
    # '1-0:42.7.0': 'Instantaneous active power L2 (-P) in kW',
    # '1-0:62.7.0': 'Instantaneous active power L3 (-P) in kW',
    # '0-1:24.2.1': 'Last 5-minute value, gas delivered in m3'
}

pattern = re.compile(b'\r\n(?=!)')

telegram = b''
checksum_found = False
good_checksum = False


try:
    ser.open()
except:
    sys.exit("Fout bij het openen van %s. Aaaaarch." % ser.name)

telegram = b''
checksum_found = False

while not checksum_found:
    # Read in a line
    telegram_line = ser.readline()
    print(str(telegram_line))

    if re.match(b'(?=!)', telegram_line):
        # print('')
        telegram = telegram + telegram_line
        checksum_found = True
    else:
        telegram = telegram + telegram_line

ser.close()


telegram_values = dict()
for telegram_line in telegram.split(b'\r\n'):
    # Split the OBIS code from the value
    # The lines with a OBIS code start with a number
    if re.match(b'\d', telegram_line):
        code = b''.join(re.split(b'(\()', telegram_line)[:1])
        value = b''.join(re.split(b'(\()', telegram_line)[1:])
        telegram_values[code] = value

#nicely print codes and convert to strings
for code, value in sorted(telegram_values.items()):
    code_string = code.decode('utf-8').strip()
    if code_string in list_of_interesting_codes:
        # Cleanup value
        clean_value = float(value.lstrip(b'\(').rstrip(b'\)*kWhA'))
        # Print nicely formatted string

        print(code_string, ': ', list_of_interesting_codes[code_string], ' - ', clean_value)

