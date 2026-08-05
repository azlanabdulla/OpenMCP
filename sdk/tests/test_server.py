from openmcp_sdk.server import OpenMCPServer
from openmcp_sdk.decorators import openmcp_tool

def test_server_creation():
    server = OpenMCPServer("test-server", "1.0.0")
    assert server.name == "test-server"
    assert server.version == "1.0.0"

def test_tool_decorator():
    server = OpenMCPServer("test", "1.0")
    
    @openmcp_tool("add", "Add two numbers")
    def add(a: int, b: int) -> int:
        return a + b
        
    server.register_tool(add)
    
    assert "add" in server.tools
    tool_info = server.tools["add"]
    assert tool_info["name"] == "add"
    assert tool_info["description"] == "Add two numbers"
    assert "a" in tool_info["inputSchema"]["properties"]
    assert "b" in tool_info["inputSchema"]["properties"]
