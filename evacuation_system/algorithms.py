"""Core algorithms: Dijkstra and BFS."""

import heapq
import math
from collections import defaultdict, deque
from typing import Optional

from .constants import MAX_ACCEPTABLE_DANGER, MobilityType, RoadStatus, ZoneType
from .graph import EvacuationGraph
from .models import EvacuationPath, PriorityQueueEntry, ReachabilityResult, Road


def dijkstra(
    graph: EvacuationGraph,
    source_id: str,
    target_id: str,
    mobility: MobilityType = MobilityType.VEHICLE,
    max_danger_threshold: float = 10.0,
) -> Optional[EvacuationPath]:
    if source_id not in graph.locations or target_id not in graph.locations:
        return None
    if not graph.locations[source_id].is_active:
        return None

    dist: dict[str, float] = defaultdict(lambda: math.inf)
    dist[source_id] = 0.0
    heap = [PriorityQueueEntry(cost=0.0, location_id=source_id, path=[source_id], roads_used=[])]
    visited: set[str] = set()

    while heap:
        entry = heapq.heappop(heap)
        current_cost = entry.cost
        current_id = entry.location_id

        if current_id in visited:
            continue
        visited.add(current_id)

        if current_id == target_id:
            roads: list[Road] = entry.roads_used
            time_h = sum(road.travel_time(mobility) for road in roads)
            dist_km = sum(road.distance_km for road in roads)
            dangers = [road.danger_score for road in roads] if roads else [0.0]
            warnings = []

            if max(dangers) >= MAX_ACCEPTABLE_DANGER:
                warnings.append(f"High danger segment detected (score {max(dangers):.1f}/10)")
            if any(road.status == RoadStatus.DAMAGED for road in roads):
                warnings.append("Route includes damaged road segments, so travel speed is reduced")

            return EvacuationPath(
                source_id=source_id,
                target_id=target_id,
                path=entry.path,
                roads=roads,
                total_cost=current_cost,
                total_time_h=time_h,
                total_dist_km=dist_km,
                max_danger=max(dangers),
                avg_danger=sum(dangers) / len(dangers),
                mobility=mobility,
                warnings=warnings,
            )

        for edge_cost, neighbor_id, road in graph.get_active_neighbors(current_id, mobility):
            if neighbor_id in visited:
                continue
            if road.danger_score > max_danger_threshold:
                continue

            new_cost = current_cost + edge_cost
            if new_cost < dist[neighbor_id]:
                dist[neighbor_id] = new_cost
                heapq.heappush(
                    heap,
                    PriorityQueueEntry(
                        cost=new_cost,
                        location_id=neighbor_id,
                        path=entry.path + [neighbor_id],
                        roads_used=entry.roads_used + [road],
                    ),
                )

    return None


def dijkstra_all_safe_zones(
    graph: EvacuationGraph,
    source_id: str,
    mobility: MobilityType = MobilityType.VEHICLE,
    max_danger_threshold: float = 10.0,
) -> list[EvacuationPath]:
    results = []
    for zone in graph.get_safe_zones():
        path = dijkstra(graph, source_id, zone.id, mobility, max_danger_threshold)
        if path is not None:
            results.append(path)
    return sorted(results, key=lambda path: path.total_cost)


def bfs_reachability(
    graph: EvacuationGraph,
    source_id: str,
    max_hops: int = 10,
    mobility: MobilityType = MobilityType.VEHICLE,
) -> ReachabilityResult:
    visited: dict[str, int] = {source_id: 0}
    queue: deque[tuple[str, int]] = deque([(source_id, 0)])

    while queue:
        current_id, hops = queue.popleft()
        if hops >= max_hops:
            continue

        for _cost, neighbor_id, _road in graph.get_active_neighbors(current_id, mobility):
            if neighbor_id not in visited:
                visited[neighbor_id] = hops + 1
                queue.append((neighbor_id, hops + 1))

    all_safe_ids = [loc.id for loc in graph.get_safe_zones()]
    reachable_safe = [safe_id for safe_id in all_safe_ids if safe_id in visited]
    unreachable_safe = [safe_id for safe_id in all_safe_ids if safe_id not in visited]

    return ReachabilityResult(
        source_id=source_id,
        reachable=visited,
        reachable_safe=reachable_safe,
        unreachable_safe=unreachable_safe,
        max_hops_used=max_hops,
    )


def bfs_nearest_safe_zone(
    graph: EvacuationGraph,
    source_id: str,
    mobility: MobilityType = MobilityType.VEHICLE,
) -> Optional[str]:
    visited: set[str] = {source_id}
    queue: deque[str] = deque([source_id])

    while queue:
        current_id = queue.popleft()
        loc = graph.locations.get(current_id)
        if loc and loc.zone_type == ZoneType.SAFE_ZONE and loc.is_active and not loc.is_full:
            return current_id

        for _cost, neighbor_id, _road in graph.get_active_neighbors(current_id, mobility):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(neighbor_id)

    return None
