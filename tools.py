#!/usr/bin/python3.12
from datetime import datetime
from pathlib import Path
from json import load

__location__ = Path(__file__).parent.resolve()

def ts_print(line: str) -> None:
    print("{}: {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), line))

def read_json(file_name: str, path: Path = __location__) -> str:
    with open(path / f"{file_name}.json", 'r', encoding="utf-8") as r_json:
        return load(r_json)