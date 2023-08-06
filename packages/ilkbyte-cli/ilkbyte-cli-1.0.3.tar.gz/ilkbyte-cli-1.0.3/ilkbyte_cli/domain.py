import typer
from ilkbyte.utils import DNSRecordType

from ilkbyte_cli.callback import raw
from ilkbyte_cli.utils import get_client, cli_pretty

domain_app = typer.Typer(name='domain', callback=raw)


@domain_app.command(name='list')
def list(page_number: int = 1):
    client = get_client()
    response = client.get_domains(page_number)

    cli_pretty({
        'domains': 'data.domain_list',
    }, response=response)


@domain_app.command()
def create(domain: str, server_name: str, ipv6: bool = False):
    client = get_client()
    response = client.create_domain(domain, server_name, ipv6)

    cli_pretty({
        'create domain': 'message',
    }, response=response)


@domain_app.command()
def record(domain: str):
    client = get_client()
    response = client.get_domain(domain)

    cli_pretty({
        'domain records': 'data.Records',
    }, response=response)


@domain_app.command()
def record_add(domain: str, record_name: str, record_type: DNSRecordType, record_content: str,
               record_priority: int):
    client = get_client()
    response = client.add_dns_record(domain, record_name, record_type, record_content, record_priority)

    cli_pretty({
        'record creating': 'data.Record',
    }, response=response)


@domain_app.command()
def record_update(domain: str, record_id: int, record_content: str, record_priority: int):
    client = get_client()
    response = client.update_dns_record(domain, record_id, record_content, record_priority)

    cli_pretty({
        'record updating': 'data.Record',
    }, response=response)


@domain_app.command()
def record_delete(domain: str, record_id: int):
    client = get_client()
    response = client.delete_dns_record(domain, record_id)

    cli_pretty({
        'record deleting': 'message',
    }, response=response)


@domain_app.command()
def record_push(domain: str):
    client = get_client()
    response = client.dns_push(domain)

    cli_pretty({
        'record pushing': 'message',
    }, response=response)


if __name__ == '__main__':
    domain_app()
