from typing import Dict
from urllib.parse import urlencode
from time import sleep

def encode_data(data: Dict) -> str:
    return urlencode(data)

def sleep_ms(ms: int):
    sleep(ms / 1000)

def format_number(number: int) -> str:
    return "{:,}".format(number)