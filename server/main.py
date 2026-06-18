from mcp.server.fastmcp import FastMCP
from databricks.sdk import WorkspaceClient
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create MCP Server
mcp = FastMCP("databricks-catalog-mcp")

# Databricks Client
w = WorkspaceClient()

# SQL Warehouse ID
WAREHOUSE_ID = os.environ.get("DATABRICKS_WAREHOUSE_ID", "c605ec288999a63d")


@mcp.tool()
def list_catalogs() -> str:
    """List all Unity Catalog catalogs."""

    try:
        catalogs = []

        for catalog in w.catalogs.list():
            catalogs.append(catalog.name)

        return json.dumps(
            {
                "status": "success",
                "catalogs": catalogs
            },
            indent=2
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_schemas(catalog_name: str) -> str:
    """List schemas in a catalog."""

    try:
        schemas = []

        for schema in w.schemas.list(
            catalog_name=catalog_name
        ):
            schemas.append(schema.name)

        return json.dumps(
            {
                "catalog": catalog_name,
                "schemas": schemas
            },
            indent=2
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_tables(
    catalog_name: str,
    schema_name: str
) -> str:
    """List tables in a schema."""

    try:
        tables = []

        for table in w.tables.list(
            catalog_name=catalog_name,
            schema_name=schema_name
        ):
            tables.append(table.name)

        return json.dumps(
            {
                "catalog": catalog_name,
                "schema": schema_name,
                "tables": tables
            },
            indent=2
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def describe_table(
    catalog_name: str,
    schema_name: str,
    table_name: str
) -> str:
    """Get table metadata."""

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

        for col in table.columns:

            columns.append(
                {
                    "name": col.name,
                    "type": str(col.type_name),
                    "nullable": getattr(
                        col,
                        "nullable",
                        None
                    )
                }
            )

        return json.dumps(
            {
                "table": full_name,
                "table_type": str(
                    table.table_type
                ),
                "columns": columns
            },
            indent=2
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


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

        result = (
            w.statement_execution
            .execute_statement(
                warehouse_id=WAREHOUSE_ID,
                statement=sql,
                wait_timeout="30s"
            )
        )

        return json.dumps(
            result.as_dict(),
            default=str
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def run_sql(query: str) -> str:
    """Execute SQL query."""

    try:

        result = (
            w.statement_execution
            .execute_statement(
                warehouse_id=WAREHOUSE_ID,
                statement=query,
                wait_timeout="30s"
            )
        )

        return json.dumps(
            result.as_dict(),
            default=str
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def count_rows(
    catalog_name: str,
    schema_name: str,
    table_name: str
) -> str:
    """Get row count from a table."""

    try:

        sql = f"""
        SELECT COUNT(*) AS total_rows
        FROM {catalog_name}.{schema_name}.{table_name}
        """

        result = (
            w.statement_execution
            .execute_statement(
                warehouse_id=WAREHOUSE_ID,
                statement=sql,
                wait_timeout="30s"
            )
        )

        return json.dumps(
            result.as_dict(),
            default=str
        )

    except Exception as e:
        return json.dumps({"error": str(e)})


def main():
    mcp.run(
        transport="streamable-http"
    )


if __name__ == "__main__":
    main()
