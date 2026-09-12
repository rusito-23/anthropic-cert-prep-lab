"""MCP server exposing an add tool and a static resource over stdio."""

import argparse
import asyncio
import logging

import mcp.types
from mcp.server import Server
from mcp.server.context import ServerRequestContext
from mcp.server.stdio import stdio_server

# Tools


class RunToolError(Exception):
    """Raised when a tool runs into an error."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def add(num1: int, num2: int) -> int:
    return num1 + num2


def divide(num1: int, num2: int) -> float:
    if num2 == 0:
        raise RunToolError("Division by zero is impossible")
    return num1 / num2


TOOLS = {
    "add": {
        "function": add,
        "description": "Executes the addition between two numbers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "num1": {"type": "integer"},
                "num2": {"type": "integer"},
            },
            "required": ["num1", "num2"],
        },
    },
    "divide": {
        "function": divide,
        "description": "Executes the division between two numbers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "num1": {"type": "integer"},
                "num2": {"type": "integer"},
            },
            "required": ["num1", "num2"],
        },
    },
}


async def list_tools(
    context: ServerRequestContext, params: mcp.types.PaginatedRequestParams | None = None
) -> mcp.types.ListToolsResult:
    logging.debug("List tools requested.")
    return mcp.types.ListToolsResult(
        tools=[
            mcp.types.Tool(
                name=name,
                description=tool.get("description"),
                input_schema=tool.get("input_schema"),
            )
            for name, tool in TOOLS.items()
        ]
    )


async def call_tool(
    context: ServerRequestContext, params: mcp.types.CallToolRequestParams | None = None
) -> mcp.types.CallToolResult:
    name = params.name
    arguments = params.arguments
    logging.debug(f"Executing tool {name} with input {arguments}")

    tool = TOOLS.get(name)
    if not tool:
        logging.error(f"Failed to retrieve tool with name {name}")
        raise ValueError(f"Unknown tool: {name}")

    try:
        result = tool.get("function")(**arguments)
        logging.debug(f"Tool execution {name} got output {result}")

        return mcp.types.CallToolResult(content=[{"type": "text", "text": f"{result}"}])

    except RunToolError as err:
        logging.error(f"Tool execution {name} failed with {err}")
        return mcp.types.CallToolResult(
            is_error=True,
            content=[{"type": "text", "text": err.message}],
        )

    except Exception as err:
        logging.error(f"Tool execution {name} failed with {err}")
        return mcp.types.CallToolResult(
            is_error=True,
            content=[{"type": "text", "text": "The operation could not be completed."}],
        )


# Resources


RESOURCES = {
    "math-ops://add/neutral": {
        "name": "get_add_neutral",
        "description": "Describes and explains the neutral number for the add.",
        "mime_type": "text/plain",
        "content": "The neutral of the add is 0. Because any number added to 0 returns itself.",
    }
}


async def list_resources(
    context: ServerRequestContext, params: mcp.types.PaginatedRequestParams | None = None
) -> mcp.types.ListResourcesResult:
    logging.debug("List resources requested.")
    return mcp.types.ListResourcesResult(
        resources=[
            mcp.types.Resource(uri=uri, name=res.get("name"), mime_type=res.get("mime_type"))
            for uri, res in RESOURCES.items()
        ]
    )


async def read_resource(
    context: ServerRequestContext, params: mcp.types.ReadResourceRequestParams | None = None
) -> mcp.types.ReadResourceResult:
    uri = params.uri
    res = RESOURCES.get(uri)
    logging.debug(f"Resource {uri} requested.")

    if not res:
        logging.error(f"Resource not found at {uri}")
        raise ValueError(f"Resource not found: {uri}")

    return mcp.types.ReadResourceResult(
        contents=[
            mcp.types.TextResourceContents(
                uri=uri, mimeType=res.get("mime_type"), text=res.get("content")
            )
        ]
    )


# Server definition


def create_server() -> Server:
    return Server(
        name="math-ops",
        version="0.0.1",
        title="Math Ops",
        description="Provides tools and resources for general math operations.",
        instructions="Use this server when math is required",
        on_list_tools=list_tools,
        on_list_resources=list_resources,
        on_call_tool=call_tool,
        on_read_resource=read_resource,
    )


# Main


# Create server
server = create_server()


async def run_server():
    async with stdio_server() as (read_stream, write_stream):
        try:
            await server.run(read_stream, write_stream, server.create_initialization_options())
        except KeyboardInterrupt:
            exit()


def main():
    # Setup logger
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    # Run server
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
