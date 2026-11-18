
from sqlalchemy import create_engine, text

# Create SQLite database connection
DATABASE_URL = "sqlite:///data/analytics.db"

engine = create_engine(DATABASE_URL, echo=True)


def get_connection():
    return engine.connect()


def create_sales_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER,
                price REAL,
                total_amount REAL,
                sale_date DATE
            )
        """))
        connection.commit()

    print("Sales table created successfully!")
