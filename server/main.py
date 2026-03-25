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
    # Databricks Apps uses port 8000 natively. 'sse' is required for Genie Code 
    mcp.run(transport="sse", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
