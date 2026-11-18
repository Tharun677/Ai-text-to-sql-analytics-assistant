import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from src.analytics import load_sales_data


def train_category_model():

    dataframe = load_sales_data()

    X = dataframe[["quantity", "price"]]
    y = dataframe["category"]

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y_encoded)

    print("\nSALES CATEGORY CLASSIFICATION")
    print("=" * 45)
    print("Model: Random Forest Classifier")
    print("Training records:", len(X))

    print("\nCATEGORY LABELS:")
    for category in encoder.classes_:
        print(category)

    return model, encoder


def predict_category(model, encoder, quantity, price):

    new_data = pd.DataFrame({
        "quantity": [quantity],
        "price": [price]
    })

    prediction = model.predict(new_data)

    return encoder.inverse_transform(prediction)[0]


if __name__ == "__main__":

    model, encoder = train_category_model()

    result = predict_category(
        model,
        encoder,
        quantity=7,
        price=15000
    )

    print("\nSAMPLE PREDICTION")
    print("Quantity: 7")
    print("Price: 15000")
    print("Predicted category:", result)
