from configparser import ConfigParser

import typer

from ilkbyte_cli.account import account_app
from ilkbyte_cli.backup import backup_app
from ilkbyte_cli.domain import domain_app
from ilkbyte_cli.server import server_app
from ilkbyte_cli.snapshot import snapshot_app
from ilkbyte_cli.utils import global_config_file

app = typer.Typer()
app.add_typer(account_app)
app.add_typer(server_app)
app.add_typer(snapshot_app)
app.add_typer(backup_app)
app.add_typer(domain_app)


@app.command(name='config', )
def configure(secret_key: str = None, access_key: str = None, host: str = 'https://api.ilkbyte.com',
              config_file: str = global_config_file):
    if secret_key is None and access_key is None:
        typer.echo('You can get api credentials on https://www.ilkbyte.com/panel/account/settings')
    if secret_key is None:
        secret_key = typer.prompt('secret_key', hide_input=True)

    if access_key is None:
        access_key = typer.prompt('access_key', hide_input=True)

    cli_section = 'cli'
    config = ConfigParser()
    config.add_section(cli_section)
    config.set(cli_section, 'host', host)
    config.set(cli_section, 'secret_key', secret_key)
    config.set(cli_section, 'access_key', access_key)

    if not config_file:
        config_file = global_config_file

    confirm = typer.confirm(f"Config will be saved to {config_file}. Do you confirm it?", abort=True)
    if confirm:
        config.write(open(config_file, 'w+'))


def main():
    app()


if __name__ == '__main__':
    main()
