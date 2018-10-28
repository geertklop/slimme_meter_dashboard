# DSMR v4.2 p1 uitlezen
# (c) 10-2012 - 2016 GJ - gratis te kopieren en te plakken
versie = "1.1"
import sys
import serial

##############################################################################
#Main program
##############################################################################
print ("DSMR P1 uitlezen",  versie)
print ("Control-C om te stoppen")
print ("Pas eventueel de waarde ser.port aan in het python script")

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
    sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)      


#Initialize
#p1_teller is mijn tellertje voor van 0 tot 36 te tellen
p1_teller=0

while p1_teller < 26:
    p1_line=''
#Read 1 line van de seriele poort
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )      
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
# als je alles wil zien moet je de volgende line uncommenten
    print (p1_line)
    p1_teller = p1_teller +1

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )      