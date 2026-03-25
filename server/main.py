from mcp.server.fastmcp import FastMCP
import json

# Create MCP server
mcp = FastMCP("mcp-sales-tools")

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
    # Databricks Apps uses port 8000 natively 
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
