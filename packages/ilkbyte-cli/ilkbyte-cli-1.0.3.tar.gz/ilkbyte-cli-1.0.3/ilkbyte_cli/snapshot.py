import typer

from ilkbyte_cli.callback import raw
from ilkbyte_cli.utils import get_client, cli_pretty

snapshot_app = typer.Typer(name='snapshot', callback=raw)


@snapshot_app.command(name='list')
def list_snapshot(server_name: str):
    client = get_client()
    response = client.get_snapshots(server_name)

    cli_pretty({
        'snapshots': 'data.snapshots',
    }, response=response)


@snapshot_app.command()
def create(server_name: str):
    client = get_client()
    response = client.create_snapshot(server_name)

    cli_pretty({
        'snapshots': 'message',
    }, response=response)


@snapshot_app.command()
def restore(server_name: str, snapshot_name: str):
    client = get_client()
    response = client.restore_snapshot(server_name, snapshot_name)

    cli_pretty({
        'snapshot restore': 'message',
    }, response=response)


@snapshot_app.command()
def update(server_name: str, snapshot_name: str):
    client = get_client()
    response = client.update_snapshot(server_name, snapshot_name)

    cli_pretty({
        'snapshot update': 'message',
    }, response=response)


@snapshot_app.command()
def delete(server_name: str, snapshot_name: str):
    client = get_client()
    response = client.delete_snapshot(server_name, snapshot_name)

    cli_pretty({
        'snapshot delete': 'message',
    }, response=response)


@snapshot_app.command()
def cron_add(server_name: str, cron_name: str, day: int, hour: int, min: int):
    client = get_client()
    response = client.set_cron(server_name, cron_name, day, hour, min)

    cli_pretty({
        'add cron': 'message',
    }, response=response)


@snapshot_app.command()
def cron_delete(server_name: str, snapshot_name: str):
    client = get_client()
    response = client.delete_cron(server_name, snapshot_name)

    cli_pretty({
        'delete cron': 'message',
    }, response=response)


if __name__ == '__main__':
    snapshot_app()
