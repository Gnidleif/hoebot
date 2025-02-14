#!/usr/bin/python3.12
from datetime import datetime

def ts_print(line: str) -> None:
    print("{}: {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), line))