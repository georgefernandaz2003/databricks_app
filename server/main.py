from mcp.server.fastmcp import FastMCP
import json

# Create MCP server
mcp = FastMCP("mcp-sales-tools", host="0.0.0.0", port=8000)

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
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()
