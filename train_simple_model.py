import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# Example: Train a simple model with mock data
X = np.array([[1], [2], [3], [4], [5]])  # Feature (e.g., time periods)
y = np.array([150, 152, 154, 156, 158])  # Target (e.g., stock prices)

model = LinearRegression()
model.fit(X, y)

# Save the model to a file
with open('simple_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Model saved successfully as 'simple_model.pkl'")
