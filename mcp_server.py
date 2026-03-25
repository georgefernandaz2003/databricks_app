from fastapi import FastAPI
import uvicorn
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("sales-tools")

@mcp.tool()
def get_sales():
    return [
        {"product": "Laptop", "sales": 120},
        {"product": "Phone", "sales": 200}
    ]

@app.get("/")
def home():
    return {"status": "MCP server running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)