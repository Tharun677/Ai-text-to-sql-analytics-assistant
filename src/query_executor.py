from sqlalchemy import text

from src.database import engine
from src.sql_generator import generate_sql
from src.sql_validator import validate_sql


def execute_query(sql_query):
    # Validate SQL before execution
    is_valid, message = validate_sql(sql_query)

    if not is_valid:
        return None, message

    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

            rows = result.fetchall()
            columns = result.keys()

            return columns, rows

    except Exception as error:
        return None, str(error)


def process_question(question):
    sql_query = generate_sql(question)

    columns, rows = execute_query(sql_query)

    return sql_query, columns, rows
