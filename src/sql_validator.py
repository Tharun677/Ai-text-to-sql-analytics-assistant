import sqlglot
from sqlglot import exp


def validate_sql(sql_query):
    """
    Validate SQL before execution.
    Only a single SELECT query is permitted.
    """

    try:
        statements = sqlglot.parse(
            sql_query,
            read="sqlite"
        )

        # Reject empty or multiple statements
        if not statements or len(statements) != 1:
            return False, "Only one SQL statement is allowed."

        statement = statements[0]

        if statement is None:
            return False, "Empty SQL statement."

        # Allow only SELECT statements
        if not isinstance(statement, exp.Select):
            return False, "Only SELECT queries are permitted."

        # Reject SELECT INTO
        if statement.args.get("into"):
            return False, "SELECT INTO is not permitted."

        return True, "SQL query validated successfully."

    except sqlglot.errors.ParseError as error:
        return False, f"Invalid SQL syntax: {error}"


if __name__ == "__main__":
    test_query = "SELECT category, SUM(total_amount) FROM sales GROUP BY category"

    is_valid, message = validate_sql(test_query)

    print("Validation result:", is_valid)
    print("Message:", message)
