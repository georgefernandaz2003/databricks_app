from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("mcp-sales-tools")

import json

@mcp.tool()
def get_sales() -> str:
    """Return sales data"""
    data = [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200},
        {"product": "Tablet", "sales": 80},
    ]
    return json.dumps(data)

def main():
    # Databricks requires HTTP transport
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
