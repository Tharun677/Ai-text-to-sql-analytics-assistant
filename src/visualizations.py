import plotly.express as px
import plotly.graph_objects as go

from src.analytics import (
    load_sales_data,
    calculate_kpis,
    category_performance,
    top_products,
    monthly_sales
)


def create_dashboard():

    # Load sales data
    dataframe = load_sales_data()

    # Calculate analytics
    kpis = calculate_kpis(dataframe)
    categories = category_performance(dataframe)
    products = top_products(dataframe).head(5)
    monthly = monthly_sales(dataframe)

    print("\nSALES ANALYTICS DASHBOARD")
    print("=" * 50)

    # Display KPIs
    print(f"Total Revenue: Rs. {kpis['total_revenue']:,.2f}")
    print(f"Total Sales: {kpis['total_sales']}")
    print(f"Total Quantity: {kpis['total_quantity']}")
    print(f"Average Sales: Rs. {kpis['average_sales']:,.2f}")

    # Chart 1: Category revenue
    category_data = categories.reset_index()

    category_chart = px.bar(
        category_data,
        x="category",
        y="total_amount",
        title="Revenue by Category",
        labels={
            "category": "Category",
            "total_amount": "Revenue (Rs.)"
        },
        text_auto=True
    )

    # Chart 2: Top five products
    product_data = products.reset_index()

    product_chart = px.bar(
        product_data,
        x="product_name",
        y="total_amount",
        title="Top 5 Products by Revenue",
        labels={
            "product_name": "Product",
            "total_amount": "Revenue (Rs.)"
        },
        text_auto=True
    )

    # Chart 3: Monthly revenue trend
    monthly_data = monthly.reset_index()

    monthly_chart = px.line(
        monthly_data,
        x="month",
        y="total_amount",
        title="Monthly Revenue Trend",
        labels={
            "month": "Month",
            "total_amount": "Revenue (Rs.)"
        },
        markers=True
    )

    # Save charts as HTML files
    category_chart.write_html("category_revenue.html")
    product_chart.write_html("top_products.html")
    monthly_chart.write_html("monthly_revenue.html")

    print("\nVISUALISATION COMPLETED")
    print("1. category_revenue.html")
    print("2. top_products.html")
    print("3. monthly_revenue.html")


if __name__ == "__main__":
    create_dashboard()
