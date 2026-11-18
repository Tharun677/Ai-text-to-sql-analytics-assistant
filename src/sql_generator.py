import re

from src.semantic_schema_search import semantic_search_schema
from src.schema_retriever import get_database_schema
from src.llm_client import ask_gemini


def generate_sql(question):
    # Retrieve relevant schema using semantic search
    schema_results = semantic_search_schema(question, limit=5)

    # Get the complete database schema
    full_schema = get_database_schema()

    # Prepare complete schema information
    schema_context = ""

    for table_name, table_info in full_schema.items():
        schema_context += f"\nTable: {table_name}\n"
        schema_context += f"Description: {table_info['description']}\n"

        for column in table_info["columns"]:
            schema_context += (
                f"- {column['column_name']} "
                f"({column['data_type']}): "
                f"{column['description']}\n"
            )

    # Prepare semantic search results
    retrieved_context = "\n".join(
        [
            f"- {item['name']} ({item['type']}): "
            f"{item['description']}"
            for item in schema_results
        ]
    )

    # Create the Gemini prompt
    prompt = f"""
You are an expert Text-to-SQL assistant.

Your task is to convert the user's question into a valid SQLite SELECT query.

DATABASE SCHEMA:
{schema_context}

SEMANTICALLY RETRIEVED SCHEMA INFORMATION:
{retrieved_context}

USER QUESTION:
{question}

RULES:
1. Generate only a valid SQLite SELECT query.
2. Use only tables and columns present in the database schema.
3. Do not invent table names or column names.
4. Use appropriate SQL functions such as SUM, AVG, COUNT and GROUP BY.
5. Do not generate INSERT, UPDATE, DELETE, DROP or other modifying queries.
6. Do not include explanations or Markdown code fences.
7. Return only the SQL query.
"""

    # Generate SQL using Gemini
    generated_sql = ask_gemini(prompt)

    if not generated_sql:
        raise ValueError("Gemini returned an empty SQL response.")

    # Remove Markdown code fences if present
    generated_sql = generated_sql.strip()
    generated_sql = re.sub(
        r"^```(?:sql)?\s*",
        "",
        generated_sql,
        flags=re.IGNORECASE
    )
    generated_sql = re.sub(r"\s*```$", "", generated_sql)

    generated_sql = generated_sql.strip()

    # Basic safety check
    if not re.match(r"^(SELECT|WITH)\b", generated_sql, re.IGNORECASE):
        raise ValueError("Gemini did not generate a SELECT query.")

    if ";" in generated_sql.rstrip(";"):
        raise ValueError("Multiple SQL statements are not allowed.")

    forbidden = re.search(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|"
        r"ATTACH|DETACH|PRAGMA)\b",
        generated_sql,
        re.IGNORECASE
    )

    if forbidden:
        raise ValueError("Unsafe SQL operation detected.")

    return generated_sql.rstrip(";")


if __name__ == "__main__":
    test_question = "Show sales by category"

    print("\nUSER QUESTION:")
    print(test_question)

    print("\nGENERATED SQL:")
    print(generate_sql(test_question))
