import datetime as dt
import sqlite3

from reader_functions.telegram_functions import *
from reader_functions.p1_uitlezen_verwerken import *

def read_extract_save():
    currentdate, verbruik1, verbruik2, verbruik2, terug1, terug2 = read_and_extract_data()

    data_to_sqlite(currentdate, verbruik1, verbruik2, verbruik2, terug1, terug2)

    return 'succes'