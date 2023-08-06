import typer

from ilkbyte_cli.callback import raw
from ilkbyte_cli.utils import get_client, cli_pretty

account_app = typer.Typer(name='account', callback=raw)


@account_app.command()
def get():
    client = get_client()
    response = client.get_account()

    cli_pretty({
        'status': 'data'
    }, response=response)


@account_app.command(name='user')
def users():
    client = get_client()
    response = client.get_users()

    cli_pretty({
        'users': 'data.user_list'
    }, response)


if __name__ == '__main__':
    account_app()
