from configparser import ConfigParser
from enum import Enum
from pathlib import Path

import typer
from ilkbyte.client import Ilkbyte
from ilkbyte.exception import ConfigurationError


class OutputFormat(str, Enum):
    plain = "plain"
    simple = "simple"
    grid = "grid"
    fancy_grid = "fancy_grid"
    pipe = "pipe"
    orgtbl = "orgtbl"
    jira = "jira"
    presto = "presto"
    pretty = "pretty"
    psql = "psql"
    rst = "rst"


home = str(Path.home())
global_config_file = f"{home}/.ilkbyte.ini"


def get_config():
    config = ConfigParser()
    config.read(global_config_file)
    if config.has_section('cli'):
        return config['cli']


def get_client():
    config = get_config()
    try:
        client = Ilkbyte(**config)
        return client
    except ConfigurationError as err:
        typer.echo(err)
        typer.secho("Enter your config by run the command: ilkbyte config")

        raise typer.Exit(2)
