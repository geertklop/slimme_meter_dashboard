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


while line_counter < 26:
    p1_line=''
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )

    p1_str = str(p1_raw)
    p1_line = p1_str.strip()

    p1_result.append(p1_line)
    line_counter += 1
    print(p1_result)


# extract result
p1_result_slicer = 0
meter = 0

while p1_result_slicer < 26:
    # verbruikt vermogen
    if p1_result[p1_result_slicer][0:9] == "1-0:1.8.1":
        daldag = float(p1_result[p1_result_slicer][10:16])

    elif p1_result[p1_result_slicer][0:9] == "1-0:1.8.2":
        piekdag = float(p1_result[p1_result_slicer][10:16])

    #teruggeleverd vermogen
    elif p1_result[p1_result_slicer][0:9] == "1-0:2.8.1":
        dalterug = float(p1_result[p1_result_slicer][10:16])

    elif p1_result[p1_result_slicer][0:9] == "1-0:2.8.2":
        piekterug = float(p1_result[p1_result_slicer][10:16])


    meter = meter + daldag + piekdag - dalterug - piekterug
    print(daldag, piekdag, dalterug, piekterug)
    p1_result_slicer += 1

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )



