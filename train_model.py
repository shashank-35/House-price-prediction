import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Set relative path to data
data_path = os.path.join("House price prediction", "house_prices.csv")
model_path = "house_model.joblib"

def train_model():
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    # Load data
    df = pd.read_csv(data_path)
    
    # Features and Target
    X = df[['area', 'bedrooms', 'age', 'distance']]
    y = df['price']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, model_path)
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
