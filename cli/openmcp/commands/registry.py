import os
import json
import tarfile
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from openmcp.client import OpenMCPClient

app = typer.Typer(help="Registry and package management commands.")
console = Console()

@app.command()
def search(query: str = typer.Argument(default="", help="Search term")):
    """
    Search for packages in the registry.
    """
    client = OpenMCPClient()
    try:
        with console.status("[cyan]Searching registry...[/cyan]"):
            packages = client.search_packages(query)
            
        if not packages:
            console.print("[yellow]No packages found.[/yellow]")
            return

        table = Table(title="OpenMCP Packages")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Verified", style="green")

        for pkg in packages:
            verified = "✅" if pkg.get("is_verified") else ""
            table.add_row(pkg.get("name"), pkg.get("description", ""), verified)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Search failed:[/bold red] {e}")

@app.command()
def publish():
    """
    Publish the package in the current directory to the registry.
    """
    cwd = Path.cwd()
    manifest_path = cwd / "manifest.json"
    
    if not manifest_path.exists():
        console.print("[bold red]Error:[/bold red] No manifest.json found in the current directory.")
        raise typer.Exit(1)

    try:
        with open(manifest_path, "r") as f:
            manifest_content = f.read()
            manifest_dict = json.loads(manifest_content)
    except Exception as e:
        console.print(f"[bold red]Error parsing manifest.json:[/bold red] {e}")
        raise typer.Exit(1)

    package_name = manifest_dict.get("name")
    if not package_name:
        console.print("[bold red]Error:[/bold red] manifest.json must contain a 'name' field.")
        raise typer.Exit(1)

    client = OpenMCPClient()
    
    # Check if package namespace exists, if not, register it
    try:
        client.get_package(package_name)
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            console.print(f"[yellow]Package namespace '{package_name}' not found. Registering...[/yellow]")
            try:
                client.register_package(package_name, description=manifest_dict.get("description", ""))
                console.print(f"[green]Successfully registered '{package_name}'.[/green]")
            except Exception as reg_err:
                console.print(f"[bold red]Failed to register namespace:[/bold red] {reg_err}")
                raise typer.Exit(1)
        else:
            console.print(f"[bold red]Error checking package:[/bold red] {e}")
            raise typer.Exit(1)

    tarball_name = f"{package_name}.tgz"
    tarball_path = cwd / tarball_name

    try:
        with console.status("[cyan]Packing directory...[/cyan]"):
            with tarfile.open(tarball_path, "w:gz") as tar:
                # Add everything in current dir, excluding the tarball itself
                for item in cwd.iterdir():
                    if item.name != tarball_name and item.name != ".git" and item.name != "mcp_modules":
                        tar.add(item, arcname=item.name)
                        
        with console.status("[cyan]Publishing to OpenMCP...[/cyan]"):
            result = client.publish_package(package_name, manifest_content, str(tarball_path))
            
        console.print(f"[bold green]Successfully published {package_name} v{manifest_dict.get('version')}![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Publish failed:[/bold red] {e}")
    finally:
        # Cleanup tarball
        if tarball_path.exists():
            tarball_path.unlink()

@app.command()
def install(package_name: str):
    """
    Install a package from the registry into the local mcp_modules directory.
    """
    client = OpenMCPClient()
    try:
        with console.status(f"[cyan]Fetching {package_name}...[/cyan]"):
            package = client.get_package(package_name)
            
        # For this prototype, we'll assume the registry returns the latest version details.
        # In a real scenario, we'd query /packages/{name}/versions to get the tarball URL.
        # Since we just have the stubbed S3, we'll simulate the download for now.
        console.print(f"[green]Found {package_name}[/green]")
        console.print(f"[cyan]Downloading... (Stubbed - would fetch from S3)[/cyan]")
        
        # Create mcp_modules dir
        install_dir = Path.cwd() / "mcp_modules" / package_name
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Write a dummy manifest to show it installed
        with open(install_dir / "manifest.json", "w") as f:
            json.dump({"name": package_name, "description": package.get("description"), "installed": True}, f)
            
        console.print(f"[bold green]Successfully installed {package_name} to ./mcp_modules/{package_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Install failed:[/bold red] {e}")
