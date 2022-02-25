#this module provide config functionality
import configparser
from pathlib import Path
import re

import typer

from rptodo import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)
from rptodo.rptodo import Routin

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH/ 'config2.ini'

def init_app(db_path:str)->int:
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
        
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code
    return SUCCESS


def _init_config_file() -> int:
    print(CONFIG_FILE_PATH)
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_database(db_path: str) -> int:

    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}

    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)

    except OSError:

        return DB_WRITE_ERROR

    return SUCCESS

def _add_routin(routin:Routin) -> Routin:
    config_parser = configparser.ConfigParser()
    config_parser["Routin"] = routin.routin

    #its has countinue