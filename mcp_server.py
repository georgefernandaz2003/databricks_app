import os
import uvicorn
from fastapi import FastAPI
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

# Create FastAPI app
app = FastAPI()

# Mount MCP endpoint at /mcp
app.mount("/mcp", mcp.sse_app())

@app.get("/")
def health():
    return {"status": "running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)