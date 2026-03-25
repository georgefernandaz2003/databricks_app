import os
import uvicorn
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("mcp-sales-tools")

@mcp.tool()
def get_sales():
    """Return sales data"""
    return [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200},
        {"product": "Tablet", "sales": 80}
    ]

# IMPORTANT: expose MCP server directly
app = mcp.sse_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)