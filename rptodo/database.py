import configparser
import datetime
import json
from os import error, read
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from rptodo import  DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, JSON_ERROR
from datetime import datetime


class DBResponse(NamedTuple):
    todo_list:Dict[datetime, List[Dict[str, Any]]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path:Path) -> None:
        self._db_path = db_path
    
    def read_todos(self) ->DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                    
                except json.JSONDecodeError:
                    return DBResponse({}, JSON_ERROR)
        except OSError:
            return DBResponse({}, DB_READ_ERROR)


    def write_todos(self, todo_list: List[Dict[str, Any]])->DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list ,SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)



DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "."+Path.home().stem+"_todo2.json"
)

def get_database_path(config_file: Path) -> Path:
    "Return the current path to the to-do database"
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    "create the to-do database."
    try:
        db_path.write_text("{}")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
