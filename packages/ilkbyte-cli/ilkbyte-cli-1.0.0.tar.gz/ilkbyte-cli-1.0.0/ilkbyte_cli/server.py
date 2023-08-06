from typing import Optional

import typer
from ilkbyte.utils import PowerAction

from ilkbyte_cli.utils import get_client

server_app = typer.Typer(name='server')


@server_app.command()
def list_all(page_number: int = 1):
    client = get_client()
    typer.echo(client.get_all_servers(page_number))


@server_app.command()
def list_active(page_number: int = 1):
    client = get_client()
    typer.echo(client.get_active_servers(page_number))


@server_app.command()
def list_plans():
    client = get_client()
    typer.echo(client.get_plans())


@server_app.command()
def create(username: str, server_name: str, os_id: int, app_id: int, package_id: int, sshkey: str,
           password: Optional[str] = None):
    client = get_client()
    typer.echo(client.create_server(username, server_name, os_id, app_id, package_id, sshkey, password))


@server_app.command()
def status(server_name: str):
    client = get_client()
    typer.echo(client.get_server(server_name))


@server_app.command()
def power(server_name: str, action: PowerAction):
    client = get_client()
    typer.echo(client.set_power(server_name, action))


@server_app.command()
def ip_list(server_name: str):
    client = get_client()
    typer.echo(client.get_ips(server_name))


@server_app.command()
def ip_logs(server_name: str):
    client = get_client()
    typer.echo(client.get_ip_logs(server_name))


@server_app.command()
def ip_logs(server_name: str, ip: str, rdns: str):
    client = get_client()
    typer.echo(client.get_ip_rdns(server_name, ip, rdns))



if __name__ == '__main__':
    server_app()
