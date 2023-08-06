import typer

from ilkbyte_cli.utils import get_client

account_app = typer.Typer(name='account')


@account_app.command()
def get():
    client = get_client()
    typer.echo(client.get_account())


@account_app.command(name='user')
def users():
    client = get_client()
    typer.echo(client.get_users())


if __name__ == '__main__':
    account_app()
