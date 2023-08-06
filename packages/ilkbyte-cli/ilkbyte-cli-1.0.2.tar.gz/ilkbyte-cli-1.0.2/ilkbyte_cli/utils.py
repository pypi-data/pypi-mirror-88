from configparser import ConfigParser
from enum import Enum
from pathlib import Path

import typer
from dotty_dict import dotty
from ilkbyte.client import Ilkbyte
from ilkbyte.exception import ConfigurationError
from tabulate import tabulate

from ilkbyte_cli.callback import state


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


def cli_pretty(message: dict, response: dict):
    if not state['raw']:
        dotty_response = dotty(response)
        try:
            for k, v in message.items():
                typer.echo('=' * len(k))
                typer.echo(k)
                typer.echo('=' * len(k))

                error = dotty_response.get('error')
                if error is not None:
                    typer.secho(error, bg=typer.colors.RED, fg=typer.colors.BRIGHT_WHITE)
                elif v == 'message':
                    if error:
                        typer.secho(error, bg=typer.colors.RED, fg=typer.colors.BRIGHT_WHITE)
                    else:
                        typer.echo(dotty_response.get(v))
                elif isinstance(dotty_response.get(v), list):
                    typer.echo(tabulate(dotty_response.get(v), headers='keys', tablefmt='psql'))
                elif isinstance(dotty_response.get(v), dict):
                    typer.echo(tabulate([dotty_response.get(v)], headers='keys', tablefmt='psql'))
                elif isinstance(dotty_response.get(v), str):
                    typer.echo(dotty_response.get(v))
                else:
                    typer.echo(response)
        except Exception as _:
            typer.echo(response)

    else:
        typer.echo(response)
