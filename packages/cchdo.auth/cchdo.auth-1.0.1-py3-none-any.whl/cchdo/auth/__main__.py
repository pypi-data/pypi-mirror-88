import click


@click.group()
def cli():
    ...


@cli.command()
@click.argument("apikey")
def apikey(apikey):
    """Write the API key to the config file, creating if needed"""
    from . import _check_apikey
    from . import write_apikey
    from . import CONFIG_FILE

    try:
        _check_apikey(apikey)
    except ValueError:
        click.echo("The API key provided doesn't look valid")
        raise click.Abort
    write_apikey(apikey)
    click.echo(f"API Key written to {CONFIG_FILE}")


if __name__ == "__main__":
    cli()
