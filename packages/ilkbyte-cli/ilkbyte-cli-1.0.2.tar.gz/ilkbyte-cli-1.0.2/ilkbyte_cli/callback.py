import typer

state = {'raw': False}


def raw(ctx: typer.Context, raw: bool = False):
    """
    Manage users in the awesome CLI app.
    """
    if raw:
        state["raw"] = True


def verbose(verbose: int = typer.Option(0, "--verbose", "-v", count=True)):
    typer.echo(f"Verbose level is {verbose}")
