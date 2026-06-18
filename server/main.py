from mcp.server.fastmcp import FastMCP
from databricks.sdk import WorkspaceClient
import json

# --------------------------------------------------
# MCP Server
# --------------------------------------------------

mcp = FastMCP("databricks-catalog-mcp")

# --------------------------------------------------
# Databricks Client
# --------------------------------------------------

w = WorkspaceClient()

# Replace with your SQL Warehouse ID
WAREHOUSE_ID = "c605ec288999a63d"

# --------------------------------------------------
# Catalog Tools
# --------------------------------------------------

@mcp.tool()
def list_catalogs() -> str:
    """List all Unity Catalog catalogs."""

    try:
        catalogs = [c.name for c in w.catalogs.list()]

        return json.dumps(
            {
                "status": "success",
                "catalogs": catalogs
            },
            indent=2
        )

    except Exception as e:
        return f"Error listing catalogs: {str(e)}"


@mcp.tool()
def list_schemas(catalog_name: str) -> str:
    """List schemas in a catalog."""

    try:

        schemas = [
            s.name
            for s in w.schemas.list(
                catalog_name=catalog_name
            )
        ]

        return json.dumps(
            {
                "catalog": catalog_name,
                "schemas": schemas
            },
            indent=2
        )

    except Exception as e:
        return f"Error listing schemas: {str(e)}"


@mcp.tool()
def list_tables(
    catalog_name: str,
    schema_name: str
) -> str:
    """List tables in a schema."""

    try:

        tables = [
            t.name
            for t in w.tables.list(
                catalog_name=catalog_name,
                schema_name=schema_name
            )
        ]

        return json.dumps(
            {
                "catalog": catalog_name,
                "schema": schema_name,
                "tables": tables
            },
            indent=2
        )

    except Exception as e:
        return f"Error listing tables: {str(e)}"


@mcp.tool()
def describe_table(
    catalog_name: str,
    schema_name: str,
    table_name: str
) -> str:
    """Describe a table."""

    try:

        full_name = (
            f"{catalog_name}."
            f"{schema_name}."
            f"{table_name}"
        )

        table = w.tables.get(
            full_name=full_name
        )

        columns = []

        if table.columns:
            for col in table.columns:
                columns.append(
                    {
                        "name": col.name,
                        "type": str(col.type_name)
                    }
                )

        return json.dumps(
            {
                "table": full_name,
                "columns": columns
            },
            indent=2
        )

    except Exception as e:
        return f"Error describing table: {str(e)}"


# --------------------------------------------------
# SQL Tools
# --------------------------------------------------

@mcp.tool()
def preview_table(
    catalog_name: str,
    schema_name: str,
    table_name: str,
    limit: int = 10
) -> str:
    """Preview rows from a table."""

    try:

        sql = f"""
        SELECT *
        FROM {catalog_name}.{schema_name}.{table_name}
        LIMIT {limit}
        """

        result = w.statement_execution.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=sql,
            wait_timeout="30s"
        )

        return json.dumps(
            result.as_dict(),
            default=str,
            indent=2
        )

    except Exception as e:
        return f"Error previewing table: {str(e)}"


@mcp.tool()
def count_rows(
    catalog_name: str,
    schema_name: str,
    table_name: str
) -> str:
    """Count rows in a table."""

    try:

        sql = f"""
        SELECT COUNT(*) AS total_rows
        FROM {catalog_name}.{schema_name}.{table_name}
        """

        result = w.statement_execution.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=sql,
            wait_timeout="30s"
        )

        return json.dumps(
            result.as_dict(),
            default=str,
            indent=2
        )

    except Exception as e:
        return f"Error counting rows: {str(e)}"


@mcp.tool()
def run_sql(query: str) -> str:
    """Run any SQL query."""

    try:

        result = w.statement_execution.execute_statement(
            warehouse_id=WAREHOUSE_ID,
            statement=query,
            wait_timeout="30s"
        )

        return json.dumps(
            result.as_dict(),
            default=str,
            indent=2
        )

    except Exception as e:
        return f"Error executing query: {str(e)}"


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@mcp.tool()
def health_check() -> str:
    """Verify MCP Server is running."""

    return "Databricks Catalog MCP Server is healthy."


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()