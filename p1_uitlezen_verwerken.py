import sys
import serial
import re
import datetime as dt
import sqlite3

from telegram_functions import *

list_of_interesting_codes = {
    '1-0:1.8.1': 'total_received_1',
    '1-0:1.8.2': 'total_received_2',
    '1-0:2.8.1': 'total_delivered_1',
    '1-0:2.8.2': 'total_delivered_2',
}

#get current date/time
currentdate = dt.datetime.now()

# get current reading
raw_telegram = read_telegram()
telegram_dict = telegram_to_dict(raw_telegram)
values_dict = extract_interesting_codes(telegram_dict,
                                        list_of_interesting_codes
                                        )

verbruik1 = values_dict['1-0:1.8.1']
verbruik2 = values_dict['1-0:1.8.2']
terug1 = values_dict['1-0:2.8.1']
terug2 = values_dict['1-0:2.8.2']

#connect to db
db = sqlite3.connect('../data/meterdata.db')
cursor = db.cursor()

# select last row
cursor.execute('''SELECT * FROM meterstanden ORDER BY id DESC LIMIT 1''')
for row in cursor:
    verbruik1_last = row[2]
    verbruik2_last = row[3]
    terug1_last = row[4]
    terug2_last = row[5]

# calculate deltas
verbruik_delta = (verbruik1 - verbruik1_last) + (verbruik2 - verbruik2_last)
terug_delta = (terug1 - terug1_last) + (terug2 - terug2_last)

# insert new data into table
query = """
        INSERT INTO meterstanden(currentdate, verbruik1, verbruik2, terug1, terug2, verbruik_delta, terug_delta)
        VALUES(?,?,?,?,?,?,?)
        """

cursor.execute(query, (currentdate,
                       verbruik1,
                       verbruik2,
                       terug1,
                       terug2,
                       verbruik_delta,
                       terug_delta))

db.commit()
db.close()



