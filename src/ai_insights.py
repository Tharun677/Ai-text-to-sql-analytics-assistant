from src.analytics import (
    load_sales_data,
    calculate_kpis,
    category_performance,
    top_products,
    monthly_sales
)

from src.llm_client import ask_gemini


def generate_business_insights():

    # Load sales data
    dataframe = load_sales_data()

    # Calculate analytics
    kpis = calculate_kpis(dataframe)
    categories = category_performance(dataframe)
    products = top_products(dataframe)
    monthly = monthly_sales(dataframe)

    # Identify top performers
    best_category = categories.idxmax()
    best_product = products.idxmax()

    # Prepare business information
    business_summary = f"""
    Total Revenue: Rs. {kpis['total_revenue']:,.2f}
    Total Sales Records: {kpis['total_sales']}
    Total Quantity Sold: {kpis['total_quantity']}
    Average Sales Value: Rs. {kpis['average_sales']:,.2f}

    Category Revenue:
    {categories.to_string()}

    Top Products:
    {products.head(5).to_string()}

    Monthly Revenue:
    {monthly.to_string()}
    """

    # Display analytics
    print("\nBUSINESS ANALYTICS SUMMARY")
    print("=" * 50)
    print(business_summary)

    # Create Gemini prompt
    prompt = f"""
    You are a professional business data analyst.

    Analyse the following sales data.

    {business_summary}

    Provide:
    1. Three important business insights.
    2. Three practical business recommendations.
    3. A short explanation of the monthly revenue trend.

    Use simple professional language.

    Important:
    - Use only the information provided.
    - Do not invent statistics or missing data.
    - Mention limitations when the dataset is small.
    """

    # Generate AI insights
    print("\nGEMINI AI BUSINESS INSIGHTS")
    print("=" * 50)

    try:
        ai_response = ask_gemini(prompt)

        print(ai_response)

        return ai_response

    except Exception as error:
        print("Gemini could not generate insights.")
        print("Reason:", error)

        print("\nFALLBACK ANALYTICS")
        print("Highest revenue category:", best_category)
        print("Top-performing product:", best_product)

        return None


if __name__ == "__main__":
    generate_business_insights()
