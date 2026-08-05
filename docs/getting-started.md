# Getting Started

## Building a Tool

Use the `openmcp-sdk` to quickly build an MCP server.

```python
from openmcp_sdk import OpenMCPServer, openmcp_tool

server = OpenMCPServer("weather-bot", "1.0.0")

@openmcp_tool("weather", "Get the current weather")
def get_weather(location: str) -> str:
    return f"The weather in {location} is beautiful!"

server.register_tool(get_weather)
server.run_stdio()
```

## Publishing your Tool

Once your tool is ready, use the OpenMCP CLI to publish it to the registry.

```bash
openmcp auth login
openmcp publish
```
