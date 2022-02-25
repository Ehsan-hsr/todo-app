from asyncore import read
from copy import error
import typer
from typing import List, Optional

from rptodo import __app_name__, __version__, ERRORS, config, database
from rptodo.rptodo import Todoer
from pathlib import Path

import rptodo
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



app = typer.Typer()


def get_todoer()->Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_file = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            "could not find config file run rptodo init.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_file.exists():
        return Todoer(db_file)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)



@app.command()
def add(
    description:List[str]=typer.Argument(...),
    priority:int=typer.Option(2,"--priority","-p", min=1, max=3),
    day:datetime=typer.Argument(...)
    ) -> None:
    todoer = get_todoer()
    dtime, todo, error = todoer.add(description, priority, day.date())
    if error:
        typer.secho(
            f"adding to-do  failed with {ERRORS[error]}",
            fg=typer.colors.RED
        )
    else:
        typer.secho(
            f"""to do {todo['Description']} added"""
            f""" in {dtime}.""",
            fg=typer.colors.GREEN
        )


@app.command(name="list")
def list_all()->None:
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    is_done = typer.style("good", fg=typer.colors.GREEN, bold=True)
    not_done = typer.style("...WAITING", fg=typer.colors.RED, bold=True)

    for day in todo_list:
        if len(todo_list[day]) >0 : print(day,":")
        for todo in todo_list[day]:
            desc_text = "   "
            desc_text += "*"*todo["Priority"]
            desc_text += todo["Description"]
            if todo["Done"]:
                desc_text = desc_text + is_done
            else:
                desc_text = desc_text + not_done
            
            typer.echo(desc_text)
        print()
        print()
        


@app.command()
def init(db_path:str = typer.Option(
    str(database.DEFAULT_DB_FILE_PATH),
    "--dbdb-path",
    "-db",
    prompt="to-do database location?",
),
) -> None:
    """Initialize the to-do database"""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'creating database failed with "{ERRORS[db_init_error]}"',
            fg= typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)


def _version_callback(value:bool)->None:
    if value:
        typer.secho(f'{__app_name__}  {__version__}')
        raise typer.Exit(1)


@app.callback()
def main(
    version:Optional[bool]=typer.Option(
        None,
        "--version",
        "-v",
        help="shoe application version and exit",
        callback=_version_callback,
        is_eager=True
    )
)->None:
    return