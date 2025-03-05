import numpy as np
import joblib
import folium
from django.shortcuts import render, redirect

# Load trained KMeans model and scaler
kmeans = joblib.load("prediction/ml_models/kmeans_model(2).pkl")  
scaler = joblib.load("prediction/ml_models/scaler(2).pkl")  

# # Simulated previous hotspot data (Replace with database storage later)
# previous_hotspots = [
#     {"latitude": 12.9716, "longitude": 77.5946, "cluster": 1},  # Example hotspot
#     {"latitude": 28.7041, "longitude": 77.1025, "cluster": 2},  # Example hotspot
# ]

# # Store the latest prediction globally (temporary, replace with database)
# latest_prediction = {}

# def predict_future_hotspot(request):
#     global latest_prediction  # Store prediction temporarily

#     if request.method == "POST":
#         latitude = float(request.POST.get("latitude"))
#         longitude = float(request.POST.get("longitude"))
#         no_of_vehicles = int(request.POST.get("no_of_vehicles"))
        
#         severity_fatal = int(request.POST.get("severity_fatal"))
#         severity_grievous = int(request.POST.get("severity_grievous"))
        
#         road_type_nh = int(request.POST.get("road_type_nh"))
#         road_type_residential = int(request.POST.get("road_type_residential"))
        
#         weather_clear = int(request.POST.get("weather_clear"))
#         weather_cloudy = int(request.POST.get("weather_cloudy"))
#         weather_heavy_rain = int(request.POST.get("weather_heavy_rain"))
#         weather_light_rain = int(request.POST.get("weather_light_rain"))
        
#         # Prepare input data
#         new_input = np.array([[latitude, longitude, no_of_vehicles, severity_fatal, 
#                                severity_grievous, road_type_nh, road_type_residential, 
#                                weather_clear, weather_cloudy, weather_heavy_rain, weather_light_rain]])

#         # Scale the input data
#         new_input_scaled = scaler.transform(new_input)

#         # Predict the cluster
#         predicted_cluster = kmeans.predict(new_input_scaled)[0]

#         # Store prediction
#         latest_prediction = {
#             "latitude": latitude,
#             "longitude": longitude,
#             "cluster": predicted_cluster
#         }

#         return redirect("prediction_result")  # Redirect to result page

#     return render(request, "form.html")

from django.shortcuts import render, redirect
from .models import AccidentPrediction  # Import the model

def predict_future_hotspot(request):
    if request.method == "POST":
        latitude = float(request.POST.get("latitude"))
        longitude = float(request.POST.get("longitude"))
        no_of_vehicles = int(request.POST.get("no_of_vehicles"))
        
        severity_fatal = int(request.POST.get("severity_fatal"))
        severity_grievous = int(request.POST.get("severity_grievous"))
        
        road_type_nh = int(request.POST.get("road_type_nh"))
        road_type_residential = int(request.POST.get("road_type_residential"))
        
        weather_clear = int(request.POST.get("weather_clear"))
        weather_cloudy = int(request.POST.get("weather_cloudy"))
        weather_heavy_rain = int(request.POST.get("weather_heavy_rain"))
        weather_light_rain = int(request.POST.get("weather_light_rain"))
        
        # Prepare input data
        new_input = np.array([[latitude, longitude, no_of_vehicles, severity_fatal, 
                               severity_grievous, road_type_nh, road_type_residential, 
                               weather_clear, weather_cloudy, weather_heavy_rain, weather_light_rain]])

        # Scale the input data
        new_input_scaled = scaler.transform(new_input)

        # Predict the cluster
        predicted_cluster = kmeans.predict(new_input_scaled)[0]

        # Save to database
        hotspot = AccidentPrediction(latitude=latitude, longitude=longitude, cluster=predicted_cluster)
        hotspot.save()

        # Redirect to result page
        return redirect("prediction_result")

    return render(request, "form.html")

from django.shortcuts import render
from .models import AccidentPrediction  # Import the database model

def prediction_result(request):
    # Fetch the latest prediction from the database
    latest_prediction = AccidentPrediction.objects.latest('timestamp') if AccidentPrediction.objects.exists() else None

    if latest_prediction:
        context = {
            "latitude": latest_prediction.latitude,
            "longitude": latest_prediction.longitude,
            "cluster": latest_prediction.cluster,
        }
    else:
        context = {"error": "No predictions available yet."}

    return render(request, "result.html", context)

# def map_view(request):
#     global latest_prediction

#     # Create a Folium map centered on the predicted location
#     accident_map = folium.Map(location=[latest_prediction["latitude"], latest_prediction["longitude"]], zoom_start=12)

#     # Mark the predicted accident location
#     folium.Marker(
#         [latest_prediction["latitude"], latest_prediction["longitude"]],
#         popup=f"Predicted Hotspot: Cluster {latest_prediction['cluster']}",
#         icon=folium.Icon(color="red")
#     ).add_to(accident_map)

#     # Plot previous hotspot clusters
#     for hotspot in previous_hotspots:
#         folium.Marker(
#             [hotspot["latitude"], hotspot["longitude"]],
#             popup=f"Past Hotspot: Cluster {hotspot['cluster']}",
#             icon=folium.Icon(color="blue")
#         ).add_to(accident_map)

#     return render(request, "map.html", {"map": accident_map._repr_html_()})
# def map_view(request):
#     # Get all stored hotspots from the database
#     previous_hotspots = AccidentPrediction.objects.all()

#     # Get the latest prediction
#     latest_prediction = AccidentPrediction.objects.latest('timestamp') if AccidentPrediction.objects.exists() else None

#     # Create a Folium map
#     if latest_prediction:
#         accident_map = folium.Map(location=[latest_prediction.latitude, latest_prediction.longitude], zoom_start=12)
#         folium.Marker(
#             [latest_prediction.latitude, latest_prediction.longitude],
#             popup=f"Predicted Hotspot: Cluster {latest_prediction.cluster}",
#             icon=folium.Icon(color="red")
#         ).add_to(accident_map)
#     else:
#         accident_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)  # Default to Bangalore

#     # Add previous hotspots
#     for hotspot in previous_hotspots:
#         folium.Marker(
#             [hotspot.latitude, hotspot.longitude],
#             popup=f"Predicted Hotspot: Cluster {hotspot.cluster}",
#             icon=folium.Icon(color="blue")
#         ).add_to(accident_map)

#     return render(request, "map.html", {"map": accident_map._repr_html_()})
import folium
from django.shortcuts import render
from .models import AccidentPrediction  # Import database model

def map_view(request):
    # Get all stored hotspots from the database
    previous_hotspots = AccidentPrediction.objects.all()

    # Get the latest prediction
    latest_prediction = AccidentPrediction.objects.latest('timestamp') if AccidentPrediction.objects.exists() else None

    # Create a Folium map
    if latest_prediction:
        accident_map = folium.Map(location=[latest_prediction.latitude, latest_prediction.longitude], zoom_start=12)
        
        # Mark the latest prediction in **RED**
        folium.Marker(
            [latest_prediction.latitude, latest_prediction.longitude],
            popup=f"Latest Predicted Hotspot: Cluster {latest_prediction.cluster}",
            icon=folium.Icon(color="red", icon="info-sign")  # Red marker for latest
        ).add_to(accident_map)
    else:
        accident_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)  # Default to Bangalore

    # Add previous hotspots **EXCEPT the latest** (in BLUE)
    for hotspot in previous_hotspots:
        if latest_prediction and (hotspot.id == latest_prediction.id):
            continue  # Skip the latest one (already added in RED)
        
        folium.Marker(
            [hotspot.latitude, hotspot.longitude],
            popup=f"Previous Hotspot: Cluster {hotspot.cluster}",
            icon=folium.Icon(color="blue", icon="cloud")  # Blue marker for previous hotspots
        ).add_to(accident_map)

    return render(request, "map.html", {"map": accident_map._repr_html_()})
