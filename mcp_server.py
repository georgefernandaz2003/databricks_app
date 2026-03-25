from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sales-tools")

@mcp.tool()
def get_sales():
    return [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200}
    ]

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000)