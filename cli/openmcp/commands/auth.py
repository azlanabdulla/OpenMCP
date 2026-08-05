import typer
from rich.console import Console
from rich.prompt import Prompt

from openmcp.client import OpenMCPClient
from openmcp import config

app = typer.Typer(help="Authentication commands.")
console = Console()

@app.command()
def login():
    """
    Log in to the OpenMCP registry.
    """
    console.print("[bold cyan]Login to OpenMCP[/bold cyan]")
    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)
    
    client = OpenMCPClient()
    try:
        with console.status("[cyan]Authenticating...[/cyan]"):
            token = client.login(email, password)
        config.set_token(token)
        console.print("[bold green]Successfully logged in![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Login failed:[/bold red] {e}")

@app.command()
def logout():
    """
    Log out of the OpenMCP registry.
    """
    config.clear_token()
    console.print("[bold green]Successfully logged out![/bold green]")
