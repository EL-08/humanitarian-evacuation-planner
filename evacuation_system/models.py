"""Data models used by the evacuation route planner."""

import math
from dataclasses import dataclass, field

from .constants import (
    DANGER_WEIGHT_FACTOR,
    MAX_ACCEPTABLE_DANGER,
    MOBILITY_SPEED,
    ROAD_SPEED_PENALTY,
    TIME_WEIGHT_FACTOR,
    MobilityType,
    RoadStatus,
    ZoneType,
)


@dataclass
class Location:
    id: str
    name: str
    zone_type: ZoneType
    latitude: float
    longitude: float
    capacity: int = 0
    current_pop: int = 0
    danger_level: float = 0.0
    is_active: bool = True

    @property
    def is_full(self) -> bool:
        return self.capacity > 0 and self.current_pop >= self.capacity

    @property
    def available_slots(self) -> int | float:
        if self.capacity == 0:
            return math.inf
        return max(0, self.capacity - self.current_pop)

    def receive_evacuees(self, count: int) -> int:
        if not self.is_active or self.zone_type != ZoneType.SAFE_ZONE:
            return 0
        accepted = min(count, self.available_slots)
        self.current_pop += int(accepted)
        return int(accepted)

    def __repr__(self) -> str:
        status = "FULL" if self.is_full else f"{self.available_slots} slots"
        return f"Location({self.id}: {self.name} [{self.zone_type.value}] | {status})"


@dataclass
class Road:
    from_id: str
    to_id: str
    distance_km: float
    base_speed_kmh: float
    status: RoadStatus = RoadStatus.CLEAR
    danger_score: float = 0.0
    bidirectional: bool = True
    last_updated: str = ""

    def travel_time(self, mobility: MobilityType) -> float:
        status_penalty = ROAD_SPEED_PENALTY[self.status]
        if status_penalty == math.inf:
            return math.inf

        mobility_penalty = MOBILITY_SPEED[mobility]
        effective_speed = self.base_speed_kmh / (status_penalty * mobility_penalty)
        return self.distance_km / effective_speed

    def composite_cost(self, mobility: MobilityType) -> float:
        travel_time = self.travel_time(mobility)
        if travel_time == math.inf:
            return math.inf

        normalized_time = travel_time / 10.0
        normalized_danger = self.danger_score / 10.0
        return (TIME_WEIGHT_FACTOR * normalized_time) + (DANGER_WEIGHT_FACTOR * normalized_danger)

    def __repr__(self) -> str:
        return (
            f"Road({self.from_id}→{self.to_id} | {self.distance_km}km | "
            f"{self.status.value} | danger={self.danger_score})"
        )


@dataclass(order=True)
class PriorityQueueEntry:
    cost: float
    location_id: str = field(compare=False)
    path: list = field(compare=False, default_factory=list)
    roads_used: list = field(compare=False, default_factory=list)


@dataclass
class EvacuationPath:
    source_id: str
    target_id: str
    path: list[str]
    roads: list[Road]
    total_cost: float
    total_time_h: float
    total_dist_km: float
    max_danger: float
    avg_danger: float
    mobility: MobilityType
    warnings: list[str] = field(default_factory=list)

    @property
    def is_high_risk(self) -> bool:
        return self.max_danger >= MAX_ACCEPTABLE_DANGER

    @property
    def path_length(self) -> int:
        return len(self.path)

    def summary(self) -> str:
        risk = "HIGH RISK" if self.is_high_risk else "Acceptable risk"
        mins = int(self.total_time_h * 60)
        warning_text = f"\n  Warnings: {'; '.join(self.warnings)}" if self.warnings else ""
        return (
            f"Route: {' -> '.join(self.path)}\n"
            f"  Distance : {self.total_dist_km:.1f} km\n"
            f"  Est. Time: {mins} min ({self.total_time_h:.2f} h)\n"
            f"  Max Danger: {self.max_danger:.1f}/10  {risk}\n"
            f"  Avg Danger: {self.avg_danger:.1f}/10\n"
            f"  Composite Cost: {self.total_cost:.4f}"
            f"{warning_text}"
        )


@dataclass
class ReachabilityResult:
    source_id: str
    reachable: dict[str, int]
    reachable_safe: list[str]
    unreachable_safe: list[str]
    max_hops_used: int

    def summary(self) -> str:
        return (
            f"BFS from {self.source_id} (max {self.max_hops_used} hops):\n"
            f"  Reachable locations : {len(self.reachable)}\n"
            f"  Reachable safe zones: {len(self.reachable_safe)}\n"
            f"  Cut-off safe zones  : {len(self.unreachable_safe)}\n"
            f"  Reachable: {list(self.reachable.keys())}"
        )
