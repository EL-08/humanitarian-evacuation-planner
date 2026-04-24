"""Shared enums and constants for the evacuation route planner."""

import math
from enum import Enum


class RoadStatus(Enum):
    CLEAR = "clear"
    DAMAGED = "damaged"
    BLOCKED = "blocked"


class MobilityType(Enum):
    VEHICLE = "vehicle"
    ON_FOOT = "on_foot"
    INJURED = "injured"


class ZoneType(Enum):
    CIVILIAN = "civilian"
    SAFE_ZONE = "safe_zone"
    MEDICAL = "medical"
    CHECKPOINT = "checkpoint"
    DESTROYED = "destroyed"


MOBILITY_SPEED = {
    MobilityType.VEHICLE: 1.0,
    MobilityType.ON_FOOT: 3.5,
    MobilityType.INJURED: 8.0,
}

ROAD_SPEED_PENALTY = {
    RoadStatus.CLEAR: 1.0,
    RoadStatus.DAMAGED: 2.0,
    RoadStatus.BLOCKED: math.inf,
}

MAX_ACCEPTABLE_DANGER = 7.0
DANGER_WEIGHT_FACTOR = 0.4
TIME_WEIGHT_FACTOR = 0.6
