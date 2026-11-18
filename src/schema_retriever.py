from sqlalchemy import inspect
from src.database import engine
from src.schema_metadata import SCHEMA_METADATA


def get_database_schema():
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)

        table_metadata = SCHEMA_METADATA.get(table_name, {})

        schema[table_name] = {
            "description": table_metadata.get(
                "description", "No table description available."
            ),
            "columns": []
        }

        for column in columns:
            column_name = column["name"]

            schema[table_name]["columns"].append({
                "column_name": column_name,
                "data_type": str(column["type"]),
                "nullable": column["nullable"],
                "description": table_metadata.get(
                    "columns", {}
                ).get(
                    column_name,
                    "No column description available."
                )
            })

    return schema


def display_schema():
    schema = get_database_schema()

    print("\nDATABASE SCHEMA WITH METADATA")
    print("=" * 50)

    for table_name, table_info in schema.items():
        print(f"\nTable: {table_name}")
        print(f"Description: {table_info['description']}")

        for column in table_info["columns"]:
            print(f"\n  Column: {column['column_name']}")
            print(f"  Type: {column['data_type']}")
            print(f"  Description: {column['description']}")


if __name__ == "__main__":
    display_schema()
