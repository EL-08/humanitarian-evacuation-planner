"""Graph structure and graph update functions."""

from collections import defaultdict
from typing import Optional

from .constants import MobilityType, RoadStatus, ZoneType
from .models import Location, Road


class EvacuationGraph:
    def __init__(self):
        self.locations: dict[str, Location] = {}
        self.adjacency: dict[str, list[Road]] = defaultdict(list)

    def add_location(self, location: Location):
        self.locations[location.id] = location
        if location.id not in self.adjacency:
            self.adjacency[location.id] = []

    def add_road(self, road: Road):
        self.adjacency[road.from_id].append(road)
        if road.bidirectional:
            reverse = Road(
                from_id=road.to_id,
                to_id=road.from_id,
                distance_km=road.distance_km,
                base_speed_kmh=road.base_speed_kmh,
                status=road.status,
                danger_score=road.danger_score,
                bidirectional=False,
                last_updated=road.last_updated,
            )
            self.adjacency[road.to_id].append(reverse)

    def update_road_status(
        self,
        from_id: str,
        to_id: str,
        new_status: RoadStatus,
        new_danger: Optional[float] = None,
    ) -> int:
        updated = 0
        for road in self.adjacency.get(from_id, []):
            if road.to_id == to_id:
                road.status = new_status
                if new_danger is not None:
                    road.danger_score = new_danger
                updated += 1
        return updated

    def destroy_location(self, location_id: str):
        if location_id in self.locations:
            self.locations[location_id].is_active = False

    def get_active_neighbors(self, location_id: str, mobility: MobilityType) -> list[tuple[float, str, Road]]:
        neighbors = []
        for road in self.adjacency.get(location_id, []):
            dest = self.locations.get(road.to_id)
            if dest is None or not dest.is_active:
                continue
            cost = road.composite_cost(mobility)
            if cost < float("inf"):
                neighbors.append((cost, road.to_id, road))
        return neighbors

    def get_safe_zones(self) -> list[Location]:
        return [
            loc for loc in self.locations.values()
            if loc.zone_type == ZoneType.SAFE_ZONE and loc.is_active and not loc.is_full
        ]

    def get_civilian_zones(self) -> list[Location]:
        return [
            loc for loc in self.locations.values()
            if loc.zone_type == ZoneType.CIVILIAN and loc.is_active
        ]

    def summary(self) -> str:
        n_loc = len(self.locations)
        n_roads = sum(len(v) for v in self.adjacency.values())
        n_safe = len(self.get_safe_zones())
        n_civil = len(self.get_civilian_zones())
        blocked = sum(
            1 for roads in self.adjacency.values()
            for road in roads if road.status == RoadStatus.BLOCKED
        )
        return (
            f"Graph: {n_loc} locations | {n_roads} road segments | "
            f"{n_safe} safe zones | {n_civil} civilian zones | {blocked} blocked roads"
        )
