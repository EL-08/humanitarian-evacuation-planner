"""Sample scenario builder for the demo web app and command-line run."""

from .constants import RoadStatus, ZoneType
from .graph import EvacuationGraph
from .models import Location, Road


def build_sample_scenario() -> EvacuationGraph:
    graph = EvacuationGraph()

    locations = [
        Location("VILLAGE_A", "Al-Rashid Village", ZoneType.CIVILIAN, 36.1, 37.2, danger_level=3.0),
        Location("VILLAGE_B", "Beit Nour Village", ZoneType.CIVILIAN, 35.9, 37.1, danger_level=2.0),
        Location("TOWN_CENTER", "Hamdaniyah Town", ZoneType.CIVILIAN, 36.2, 37.5, danger_level=6.0),
        Location("CROSSROADS", "Route 7 Crossroads", ZoneType.CHECKPOINT, 35.8, 37.4, danger_level=8.5),
        Location("UN_COMPOUND", "UN Humanitarian Hub", ZoneType.SAFE_ZONE, 36.3, 38.0, capacity=500, danger_level=0.5),
        Location("REFUGEE_CAMP", "Northern Refugee Camp", ZoneType.SAFE_ZONE, 35.7, 37.8, capacity=300, danger_level=1.0),
        Location("CAMP_NORTH", "Camp Northern Outpost", ZoneType.SAFE_ZONE, 36.5, 37.4, capacity=150, danger_level=0.2),
        Location("MEDICAL_POST", "Field Medical Station", ZoneType.MEDICAL, 36.0, 37.6, danger_level=1.5),
    ]
    for location in locations:
        graph.add_location(location)

    roads = [
        Road("VILLAGE_A", "TOWN_CENTER", distance_km=8, base_speed_kmh=60, status=RoadStatus.DAMAGED, danger_score=3.0),
        Road("VILLAGE_A", "VILLAGE_B", distance_km=3, base_speed_kmh=40, status=RoadStatus.DAMAGED, danger_score=5.5),
        Road("VILLAGE_A", "CAMP_NORTH", distance_km=5, base_speed_kmh=50, status=RoadStatus.CLEAR, danger_score=3.0),
        Road("VILLAGE_B", "CROSSROADS", distance_km=15, base_speed_kmh=60, status=RoadStatus.CLEAR, danger_score=3.0),
        Road("VILLAGE_B", "MEDICAL_POST", distance_km=6, base_speed_kmh=40, status=RoadStatus.CLEAR, danger_score=5.0),
        Road("TOWN_CENTER", "UN_COMPOUND", distance_km=12, base_speed_kmh=70, status=RoadStatus.BLOCKED, danger_score=1.0),
        Road("TOWN_CENTER", "MEDICAL_POST", distance_km=4, base_speed_kmh=50, status=RoadStatus.CLEAR, danger_score=2.5),
        Road("TOWN_CENTER", "CAMP_NORTH", distance_km=14, base_speed_kmh=70, status=RoadStatus.CLEAR, danger_score=5.2),
        Road("CROSSROADS", "REFUGEE_CAMP", distance_km=15, base_speed_kmh=60, status=RoadStatus.CLEAR, danger_score=2.0),
        Road("UN_COMPOUND", "REFUGEE_CAMP", distance_km=10, base_speed_kmh=60, status=RoadStatus.CLEAR, danger_score=1.5),
        Road("MEDICAL_POST", "UN_COMPOUND", distance_km=5, base_speed_kmh=50, status=RoadStatus.CLEAR, danger_score=5.0),
        Road("MEDICAL_POST", "REFUGEE_CAMP", distance_km=4, base_speed_kmh=60, status=RoadStatus.CLEAR, danger_score=3.0),
        Road("CAMP_NORTH", "UN_COMPOUND", distance_km=4, base_speed_kmh=65, status=RoadStatus.DAMAGED, danger_score=3.8),
    ]
    for road in roads:
        graph.add_road(road)

    return graph
