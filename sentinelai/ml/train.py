import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
import joblib

# Connect to SQLite database
engine = create_engine("sqlite:///./sentinelai.db")

# Read traffic logs
df = pd.read_sql("traffic_logs", engine)

if df.empty:
    print("No data to train.")
    exit()

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Group by IP per minute (pandas compatible)
df["minute"] = df["timestamp"].dt.floor("min")

# Feature: request count per IP per minute
features = df.groupby(["ip", "minute"]).size().reset_index(name="count")

# X = request count
X = features[["count"]]

# Label: attack if count > 10
y = (features["count"] > 10).astype(int)

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "ml/model.joblib")

print("Model trained and saved successfully.")
