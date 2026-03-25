from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-sales-tools")

@mcp.tool()
def get_sales():
    """Return sales data"""
    return [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200},
        {"product": "Tablet", "sales": 80}
    ]

if __name__ == "__main__":
    mcp.run()