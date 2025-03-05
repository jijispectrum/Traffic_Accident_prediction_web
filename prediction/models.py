from django.db import models

# Create your models here.
from django.db import models

# class TrafficAccident(models.Model):
#     district = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     accident_date = models.DateField()
#     accident_time = models.TimeField()
#     weather_condition = models.CharField(max_length=50)
#     road_type = models.CharField(max_length=50)
#     vehicles_involved = models.IntegerField()
#     casualties = models.IntegerField()
#     latitude = models.FloatField()
#     longitude = models.FloatField()

#     def __str__(self):
#         return f"{self.district} - {self.accident_date}"
from django.db import models

class AccidentPrediction(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    cluster = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Stores prediction time

    def __str__(self):
        return f"Cluster {self.cluster} at ({self.latitude}, {self.longitude})"
