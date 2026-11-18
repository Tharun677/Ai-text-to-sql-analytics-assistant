
from sqlalchemy import text
from src.database import engine

def insert_sample_data():
    sales_data = [
        ("Laptop", "Electronics", 5, 50000, 250000, "2026-01-10"),
        ("Mobile", "Electronics", 10, 20000, 200000, "2026-01-12"),
        ("Chair", "Furniture", 8, 3000, 24000, "2026-01-15"),
        ("Table", "Furniture", 4, 7000, 28000, "2026-01-18"),
        ("Headphones", "Electronics", 15, 1500, 22500, "2026-01-20"),
        ("Keyboard", "Accessories", 12, 800, 9600, "2026-01-22"),
        ("Mouse", "Accessories", 20, 500, 10000, "2026-01-25"),
        ("Monitor", "Electronics", 6, 12000, 72000, "2026-01-28"),
        ("Sofa", "Furniture", 2, 25000, 50000, "2026-02-02"),
        ("Printer", "Electronics", 3, 10000, 30000, "2026-02-05")
    ]

    with engine.connect() as connection:
        connection.execute(
            text("""
                INSERT INTO sales
                (product_name, category, quantity, price, total_amount, sale_date)
                VALUES
                (:product_name, :category, :quantity, :price, :total_amount, :sale_date)
            """),
            [
                {
                    "product_name": row[0],
                    "category": row[1],
                    "quantity": row[2],
                    "price": row[3],
                    "total_amount": row[4],
                    "sale_date": row[5]
                }
                for row in sales_data
            ]
        )
        connection.commit()

    print("10 sample sales records inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()
