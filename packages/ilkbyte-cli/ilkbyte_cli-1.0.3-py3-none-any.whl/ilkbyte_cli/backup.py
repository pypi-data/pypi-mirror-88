import typer

from ilkbyte_cli.callback import raw
from ilkbyte_cli.utils import get_client, cli_pretty

backup_app = typer.Typer(name='backup', callback=raw)


@backup_app.command(name='list')
def list(server_name: str):
    client = get_client()
    response = client.get_backups(server_name)

    cli_pretty({
        'backup': 'data.backup',
    }, response=response)


@backup_app.command()
def restore(server_name: str, backup_name: str):
    client = get_client()
    response = client.restore_backup(server_name, backup_name)

    cli_pretty({
        'backup restore': 'message',
    }, response=response)


if __name__ == '__main__':
    backup_app()
