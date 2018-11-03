import sys
import serial
import re
from telegram_functions import *

list_of_interesting_codes = {
    '1-0:1.8.1': 'total_received_1',
    '1-0:1.8.2': 'total_received_2',
    '1-0:2.8.1': 'total_deliverd_1',
    '1-0:2.8.2': 'total_deliverd_2',
}

raw_telegram = read_telegram()
telegram_dict = telegram_to_dict(raw_telegram)
values_dict = extract_interesting_codes(telegram_dict,
                                        list_of_interesting_codes
                                        )

for key in values_dict.keys():
    print(key, ':', values_dict[key])
