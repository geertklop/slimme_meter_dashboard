import sys
import serial

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

#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Programma afgebroken."  % ser.name)

# line_counter is counter of lines read in serial
# p1 result = list of lines
line_counter = 0
p1_result = []


p1_line = str(ser.readLine())
print(p1_line)

# while line_counter < 26:
#     p1_line = ''
#     try:
#         p1_raw = ser.readLine()
#     except:
#         sys.exit("Seriele poort %s kan niet gelezen worden. Programma afgebroken." % ser.name)



