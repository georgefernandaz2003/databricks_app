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

@mcp.tool()
def get_product_inventory(product_name: str) -> str:
    """Return the current inventory count for a specific product."""
    # Mock inventory data
    inventory = {
        "Laptop": 45,
        "Phone": 130,
        "Tablet": 25,
        "Headphones": 210
    }
    
    # Capitalize the product name matching the dictionary
    product_name_clean = str(product_name).capitalize()
    
    if product_name_clean in inventory:
        return json.dumps({"product": product_name_clean, "stock": inventory[product_name_clean]})
    else:
        return json.dumps({"error": f"Product '{product_name}' not found in inventory."})

@mcp.tool()
def get_company_revenue_forecast(year: int) -> str:
    """Return the revenue forecast given a specific year (e.g. 2026)."""
    if year < 2024:
        return json.dumps({"error": "Forecast data is only available for 2024 onwards."})
    
    base_revenue = 1500000
    growth_rate = 0.15
    years_diff = year - 2024
    
    projected_revenue = base_revenue * ((1 + growth_rate) ** years_diff)
    return json.dumps({"year": year, "projected_revenue_usd": round(projected_revenue, 2)})

import urllib.request
import urllib.parse

@mcp.tool()
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for a given topic and return the top result summary."""
    try:
        # Ask the Wikipedia API for a search summary
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
        
        # Wikipedia requires a User-Agent header
        req = urllib.request.Request(url, headers={'User-Agent': 'Databricks-MCP-Custom-Agent/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            return json.dumps({"error": f"No Wikipedia results found for '{query}'."})
            
        # Get the first result and clean up HTML tags in the snippet
        top_result = search_results[0]
        title = top_result.get("title", "")
        snippet = top_result.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
        
        return json.dumps({
            "title": title,
            "summary": snippet,
            "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
        })
    except Exception as e:
        return json.dumps({"error": f"Wikipedia search failed: {str(e)}"})

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current temperature and weather conditions for a specific city or location."""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Databricks-MCP/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        current = data.get("current_condition", [{}])[0]
        desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        
        return json.dumps({
            "location": location,
            "condition": desc,
            "temperature_C": current.get("temp_C", "N/A"),
            "temperature_F": current.get("temp_F", "N/A"),
            "humidity_percent": current.get("humidity", "N/A"),
            "wind_speed_kmh": current.get("windspeedKmph", "N/A")
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to get weather for {location}: {str(e)}"})

@mcp.tool()
def get_random_joke() -> str:
    """Fetch a random programming, pun, or general joke."""
    try:
        url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun?safe-mode"
        req = urllib.request.Request(url, headers={'User-Agent': 'Databricks-MCP/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        if data.get("type") == "twopart":
            joke = f"{data.get('setup')} ... {data.get('delivery')}"
        else:
            joke = data.get("joke", "I'm fresh out of jokes.")
            
        return json.dumps({"joke": joke})
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch joke: {str(e)}"})

def main():
    # Databricks Apps uses port 8000 natively 
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()
