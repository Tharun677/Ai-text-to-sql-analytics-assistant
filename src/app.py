import streamlit as st
import pandas as pd
import plotly.express as px

from src.query_executor import process_question
from src.analytics import (
    load_sales_data,
    calculate_kpis,
    category_performance,
    top_products,
    monthly_sales
)
from src.ai_insights import generate_business_insights


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Text-to-SQL Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Text-to-SQL Analytics Assistant")
st.write(
    "Ask questions about your sales data in simple English "
    "and explore AI-powered business analytics."
)

st.divider()


# --------------------------------------------------
# LOAD SALES DATA
# --------------------------------------------------

try:
    sales_data = load_sales_data()

    if sales_data.empty:
        st.warning("No sales records found in the database.")
        st.stop()

    kpis = calculate_kpis(sales_data)
    categories = category_performance(sales_data)
    products = top_products(sales_data).head(5)
    monthly = monthly_sales(sales_data)

except Exception as error:
    st.error(f"Unable to load sales analytics: {error}")
    st.stop()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{kpis['total_revenue']:,.2f}"
    )

with col2:
    st.metric(
        "🧾 Total Sales Records",
        f"{kpis['total_sales']}"
    )

with col3:
    st.metric(
        "📦 Total Quantity Sold",
        f"{kpis['total_quantity']}"
    )

with col4:
    st.metric(
        "📊 Average Sales Value",
        f"₹{kpis['average_sales']:,.2f}"
    )

st.divider()


# --------------------------------------------------
# CATEGORY REVENUE CHART
# --------------------------------------------------

st.subheader("📈 Revenue by Category")

category_data = categories.reset_index()
category_data.columns = ["category", "revenue"]

category_chart = px.bar(
    category_data,
    x="category",
    y="revenue",
    color="category",
    title="Category-wise Revenue",
    text_auto=".2s",
    labels={
        "category": "Product Category",
        "revenue": "Revenue (₹)"
    }
)

st.plotly_chart(
    category_chart,
    use_container_width=True
)

st.divider()


# --------------------------------------------------
# TOP PRODUCTS CHART
# --------------------------------------------------

st.subheader("🏆 Top 5 Products")

product_data = products.reset_index()
product_data.columns = ["product_name", "revenue"]

product_chart = px.bar(
    product_data,
    x="product_name",
    y="revenue",
    title="Top 5 Products by Revenue",
    text_auto=".2s",
    labels={
        "product_name": "Product",
        "revenue": "Revenue (₹)"
    }
)

st.plotly_chart(
    product_chart,
    use_container_width=True
)

st.divider()


# --------------------------------------------------
# MONTHLY REVENUE TREND
# --------------------------------------------------

st.subheader("📅 Monthly Revenue Trend")

monthly_data = monthly.reset_index()
monthly_data.columns = ["month", "revenue"]

monthly_chart = px.line(
    monthly_data,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue Analysis",
    labels={
        "month": "Month",
        "revenue": "Revenue (₹)"
    }
)

st.plotly_chart(
    monthly_chart,
    use_container_width=True
)

st.divider()


# --------------------------------------------------
# GEMINI AI BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI-Powered Business Insights")

st.write(
    "Use Gemini to analyse your sales data "
    "and generate business recommendations."
)

if st.button("Generate AI Business Insights"):

    with st.spinner("Gemini is analysing your sales data..."):

        try:
            insights = generate_business_insights()

            if insights:
                st.markdown(insights)
            else:
                st.warning(
                    "AI insights could not be generated. "
                    "Please try again."
                )

        except Exception as error:
            st.error(f"Unable to generate insights: {error}")


st.divider()


# --------------------------------------------------
# TEXT-TO-SQL QUESTION SECTION
# --------------------------------------------------

st.subheader("💬 Ask Your Sales Data")

question = st.text_input(
    "Enter your business question:",
    placeholder="Example: Show total revenue by category"
)

if st.button("Generate Answer"):

    if question.strip():

        with st.spinner("Generating and executing SQL query..."):

            try:
                sql_query, columns, rows = process_question(question)

                st.subheader("Generated SQL Query")

                st.code(
                    sql_query,
                    language="sql"
                )

                if columns is not None:

                    st.subheader("Query Results")

                    result_data = [
                        dict(zip(columns, row))
                        for row in rows
                    ]

                    result_df = pd.DataFrame(result_data)

                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )

                    if not result_df.empty:
                        st.success(
                            f"Query executed successfully. "
                            f"{len(result_df)} result rows returned."
                        )

                else:
                    st.error(f"Query error: {rows}")

            except Exception as error:
                st.error(f"Unable to process question: {error}")

    else:
        st.warning("Please enter a business question.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Text-to-SQL Analytics Assistant | "
    "Powered by Python, SQLite, Gemini, Pandas and Plotly"
)
