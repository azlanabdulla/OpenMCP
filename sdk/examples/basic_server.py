from openmcp_sdk import OpenMCPServer, openmcp_tool

server = OpenMCPServer("example-server", "1.0.0")

@openmcp_tool("add", "Add two numbers together")
def add(a: int, b: int) -> int:
    return a + b

@openmcp_tool("weather", "Get the weather for a location")
def get_weather(location: str, unit: str = "celsius") -> str:
    return f"The weather in {location} is 22 degrees {unit}."

# Register tools with the server
server.register_tool(add)
server.register_tool(get_weather)

if __name__ == "__main__":
    # In a real environment, MCP clients interact via standard input/output
    server.run_stdio()
