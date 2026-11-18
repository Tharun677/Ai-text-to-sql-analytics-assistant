import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from src.analytics import load_sales_data


def train_sales_model():

    # Load sales dataset
    dataframe = load_sales_data()

    # Select input features and target
    X = dataframe[["quantity", "price"]]
    y = dataframe["total_amount"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Generate predictions
    predictions = model.predict(X_test)

    # Evaluate model
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\nSALES PREDICTION MODEL")
    print("=" * 40)

    print("Model: Linear Regression")
    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.4f}")

    return model


if __name__ == "__main__":
    train_sales_model()
