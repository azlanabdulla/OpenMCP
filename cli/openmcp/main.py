import typer

from openmcp.commands import auth, registry

app = typer.Typer(
    help="OpenMCP: The Open Marketplace for AI Tools.",
    no_args_is_help=True,
)

app.add_typer(auth.app, name="auth", help="Authentication commands")
app.command(name="search")(registry.search)
app.command(name="publish")(registry.publish)
app.command(name="install")(registry.install)

@app.command()
def version():
    """Show the OpenMCP CLI version."""
    typer.echo("OpenMCP CLI Version 0.1.0")

if __name__ == "__main__":
    app()
