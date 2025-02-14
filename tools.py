#!/usr/bin/python3.12
import logging
from datetime import datetime
from pathlib import Path
from json import load

__location__ = Path(__file__).parent.resolve()

def ts_print(line: str) -> None:
    print("{}: {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), line))

def read_json(file_name: str, path: Path = __location__) -> str:
    with open(path / f"{file_name}.json", 'r', encoding="utf-8") as r_json:
        return load(r_json)
    
def setup_logging() -> None:
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=__location__ / "discord.log", encoding="utf-8", mode='w')
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)