import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

# Load dataset (Update path if needed)
df = pd.read_csv("prediction/ml_models/finaltf.csv")

# Select relevant features for clustering
features = ['Latitude', 'Longitude', 'Noofvehicle_involved',
            'Severity_Fatal', 'Severity_Grievous Injury', 
            'Weather_Clear', 'Weather_Cloudy', 'Weather_Heavy Rain', 
            'Weather_Light Rain', 'Road_Type_NH', 'Road_Type_Residential Street']

# Ensure all required columns exist
df = df[features]

# Scale features using StandardScaler
scaler = StandardScaler()
features_scaled = scaler.fit_transform(df)

# Train KMeans clustering model
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(features_scaled)

# Save trained models
joblib.dump(scaler, "prediction/ml_models/scaler(2).pkl")
joblib.dump(kmeans, "prediction/ml_models/kmeans_model(2).pkl")

# Save dataset with clusters for visualization
df.to_csv("prediction/ml_models/clustered_accidents.csv", index=False)

print("Model training completed and saved.")
