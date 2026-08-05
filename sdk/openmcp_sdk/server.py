import json
import sys
import traceback
from typing import Callable, Dict, Any

class OpenMCPServer:
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Callable] = {}
        
    def register_tool(self, func: Callable):
        """Register a function decorated with @openmcp_tool"""
        if not getattr(func, "__mcp_tool__", False):
            raise ValueError(f"Function {func.__name__} must be decorated with @openmcp_tool")
            
        tool_name = func.__mcp_name__
        self.tools[tool_name] = func

    def _handle_list_tools(self) -> Dict[str, Any]:
        tools_list = []
        for name, func in self.tools.items():
            tools_list.append({
                "name": name,
                "description": func.__mcp_description__,
                "inputSchema": func.__mcp_schema__
            })
        return {"tools": tools_list}
        
    def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name not in self.tools:
            raise Exception(f"Tool not found: {name}")
            
        func = self.tools[name]
        try:
            result = func(**args)
            return {
                "content": [{"type": "text", "text": str(result)}]
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error executing tool: {str(e)}\n{traceback.format_exc()}"}],
                "isError": True
            }

    def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        req_id = request.get("id")
        
        response = {"jsonrpc": "2.0", "id": req_id}
        
        try:
            if method == "initialize":
                response["result"] = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": self.name, "version": self.version}
                }
            elif method == "tools/list":
                response["result"] = self._handle_list_tools()
            elif method == "tools/call":
                response["result"] = self._handle_call_tool(params)
            else:
                response["error"] = {"code": -32601, "message": "Method not found"}
        except Exception as e:
            response["error"] = {"code": -32603, "message": str(e)}
            
        return response

    def run_stdio(self):
        """Run the server using standard input/output for communication (JSON-RPC)"""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                request = json.loads(line)
                response = self._process_request(request)
                # MCP dictates messages are single-line JSON followed by newline on stdout
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                err = {"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}}
                sys.stdout.write(json.dumps(err) + "\n")
                sys.stdout.flush()
