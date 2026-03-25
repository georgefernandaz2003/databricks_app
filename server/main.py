from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("mcp-sales-tools")

@mcp.tool()
def get_sales():
    """Return sales data"""
    return [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200},
        {"product": "Tablet", "sales": 80},
    ]

def main():
    # Run MCP server with HTTP transport required by Databricks
    mcp.run(transport="streamable-http")
