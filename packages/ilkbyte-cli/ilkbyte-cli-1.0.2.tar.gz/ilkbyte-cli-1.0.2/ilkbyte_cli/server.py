from typing import Optional

import typer
from ilkbyte.utils import PowerAction

from ilkbyte_cli.callback import raw
from ilkbyte_cli.utils import get_client, cli_pretty

server_app = typer.Typer(name='server', callback=raw)


@server_app.command()
def list(active: bool = False, page_number: int = 1):
    if active:
        list_active(page_number)
    else:
        list_all(page_number)


def list_all(page_number: int = 1):
    client = get_client()
    response = client.get_all_servers(page_number)
    cli_pretty({
        'all servers': 'data.server_list'
    }, response=response)


def list_active(page_number: int = 1):
    client = get_client()
    response = client.get_active_servers(page_number)
    cli_pretty({
        'active servers': 'data.server_list'
    }, response=response)


@server_app.command()
def plans(app: bool = False, os: bool = False, package: bool = False):
    client = get_client()
    response = client.get_plans()

    if not app and not os and not package:
        cli_pretty({
            'application plans': 'data.application',
            'operating system plans': 'data.operating_system',
            'package plans': 'data.package'
        }, response=response)
    if app:
        cli_pretty({
            'application plans': 'data.application',
        }, response=response)
    if os:
        cli_pretty({
            'operating system plans': 'data.operating_system',
        }, response=response)
    if package:
        cli_pretty({
            'package plans': 'data.package'
        }, response=response)


@server_app.command()
def create(username: str, server_name: str, package_id: int, sshkey: str, os_id: int = 0, app_id: int = 0,
           password: Optional[str] = None):
    client = get_client()
    response = client.create_server(username, server_name, os_id, app_id, package_id, sshkey, password)

    cli_pretty({
        'server': 'data.server_info',
    }, response=response)


@server_app.command()
def status(server_name: str):
    client = get_client()
    response = client.get_server(server_name)

    cli_pretty({
        'server': 'data',
    }, response=response)


@server_app.command()
def power(server_name: str, action: PowerAction):
    client = get_client()
    response = client.set_power(server_name, action)

    cli_pretty({
        'server': 'data',
    }, response=response)


@server_app.command()
def ip(server_name: str, ipv4: bool = False, ipv6: bool = False):
    client = get_client()
    response = client.get_ips(server_name)

    if not ipv4 and not ipv6:
        cli_pretty({
            'ipv4': 'data.ipv4',
            'ipv6': 'data.ipv6',
        }, response=response)

    if ipv6:
        cli_pretty({
            'ipv6': 'data.ipv6',
        }, response=response)

    if ipv4:
        cli_pretty({
            'ipv4': 'data.ipv4',
        }, response=response)


@server_app.command()
def ip_logs(server_name: str):
    client = get_client()
    response = client.get_ip_logs(server_name)

    cli_pretty({
        'ip logs': 'data',
    }, response=response)


@server_app.command()
def ip_rdns(server_name: str, ip: str, rdns: str):
    client = get_client()
    response = client.get_ip_rdns(server_name, ip, rdns)

    cli_pretty({
        'rdns': 'data',
    }, response=response)


if __name__ == '__main__':
    server_app()
