from typer.testing import CliRunner
from openmcp.main import app

runner = CliRunner()

def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "OpenMCP Package Manager" in result.stdout
