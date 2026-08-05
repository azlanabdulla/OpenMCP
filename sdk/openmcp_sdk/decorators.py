import inspect
from functools import wraps
from pydantic import TypeAdapter

# A registry to hold tools temporarily if we use class-level decorators,
# but passing the server instance or binding is cleaner. We will attach 
# metadata to the function.

def openmcp_tool(name: str = None, description: str = None):
    """
    Decorator to mark a function as an MCP tool.
    Infers the JSON schema from Python type hints.
    """
    def decorator(func):
        tool_name = name or func.__name__
        tool_desc = description or inspect.getdoc(func) or f"Execute {tool_name}"
        
        # We can extract the schema using Pydantic's internal utilities,
        # but the simplest way is to create a dynamic Pydantic model for the kwargs.
        sig = inspect.signature(func)
        fields = {}
        for param_name, param in sig.parameters.items():
            if param.annotation == inspect.Parameter.empty:
                annotation = str
            else:
                annotation = param.annotation
                
            if param.default == inspect.Parameter.empty:
                fields[param_name] = (annotation, ...)
            else:
                fields[param_name] = (annotation, param.default)
                
        # Generate the JSON schema for this function's arguments
        from pydantic import create_model
        input_model = create_model(f"{tool_name}Input", **fields)
        schema = input_model.model_json_schema()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
            
        # Attach MCP metadata to the wrapper
        wrapper.__mcp_tool__ = True
        wrapper.__mcp_name__ = tool_name
        wrapper.__mcp_description__ = tool_desc
        wrapper.__mcp_schema__ = schema
        
        return wrapper
    return decorator
