import typer
from rich.console import Console

app = typer.Typer(
    name="openmcp",
    help="OpenMCP CLI - The Open Marketplace for AI Tools",
    no_args_is_help=True,
)
console = Console()

@app.command()
def version():
    """Print the version of OpenMCP CLI."""
    console.print("[bold green]OpenMCP CLI version 0.1.0[/bold green]")

@app.command()
def info(plugin_name: str):
    """Get information about a specific plugin."""
    console.print(f"Fetching info for [bold cyan]{plugin_name}[/bold cyan]...")
    # TODO: Implement API call
    console.print(f"Name: {plugin_name}\nStatus: Not found (API not connected)")

if __name__ == "__main__":
    app()
