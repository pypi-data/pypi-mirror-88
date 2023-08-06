from typing import Optional

import typer
from ilkbyte.utils import PowerAction

from ilkbyte_cli.utils import get_client

snapshot_app = typer.Typer(name='snapshot')


@snapshot_app.command(name='list')
def list_snapshot():
    client = get_client()
    typer.echo(client.get_snapshots())


@snapshot_app.command()
def create(name: str):
    client = get_client()
    typer.echo(client.create_snapshot(name))


if __name__ == '__main__':
    snapshot_app()
