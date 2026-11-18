import unittest

from src.sql_validator import validate_sql


class TestSQLValidator(unittest.TestCase):

    def test_valid_select_query(self):
        query = "SELECT * FROM sales"

        is_valid, message = validate_sql(query)

        self.assertTrue(is_valid)

    def test_drop_query_rejected(self):
        query = "DROP TABLE sales"

        is_valid, message = validate_sql(query)

        self.assertFalse(is_valid)

    def test_delete_query_rejected(self):
        query = "DELETE FROM sales"

        is_valid, message = validate_sql(query)

        self.assertFalse(is_valid)

    def test_multiple_statements_rejected(self):
        query = "SELECT * FROM sales; DROP TABLE sales"

        is_valid, message = validate_sql(query)

        self.assertFalse(is_valid)

    def test_invalid_sql_rejected(self):
        query = "SELECT FROM WHERE"

        is_valid, message = validate_sql(query)

        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
