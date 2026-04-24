"""High-level planning coordinator that combines BFS and Dijkstra."""

from .algorithms import bfs_nearest_safe_zone, bfs_reachability, dijkstra, dijkstra_all_safe_zones
from .constants import MAX_ACCEPTABLE_DANGER, MobilityType
from .graph import EvacuationGraph
from .models import EvacuationPath


class EvacuationPlanner:
    def __init__(self, graph: EvacuationGraph):
        self.graph = graph
        self.plans: list[EvacuationPath] = []

    def plan_single_evacuation(
        self,
        source_id: str,
        mobility: MobilityType = MobilityType.VEHICLE,
        group_size: int = 1,
        prefer_safety: bool = True,
    ) -> dict:
        result = {
            "source_id": source_id,
            "group_size": group_size,
            "mobility": mobility.value,
            "path": None,
            "fallback": False,
            "reachability": None,
            "message": "",
        }

        reach = bfs_reachability(self.graph, source_id, max_hops=15, mobility=mobility)
        result["reachability"] = reach

        if not reach.reachable_safe:
            result["message"] = (
                f"CRITICAL: No safe zones reachable from {source_id}. "
                f"Location may be completely surrounded."
            )
            return result

        danger_limit = MAX_ACCEPTABLE_DANGER if prefer_safety else 10.0
        path = dijkstra(self.graph, source_id, reach.reachable_safe[0], mobility, danger_limit)

        if path is None or self.graph.locations[path.target_id].is_full:
            all_paths = dijkstra_all_safe_zones(self.graph, source_id, mobility, danger_limit)
            for candidate in all_paths:
                if not self.graph.locations[candidate.target_id].is_full:
                    path = candidate
                    break

        if path is None and prefer_safety:
            result["fallback"] = True
            path = dijkstra(self.graph, source_id, reach.reachable_safe[0], mobility, max_danger_threshold=10.0)
            if path:
                path.warnings.append("Danger threshold relaxed, so this route carries elevated risk")

        if path is None:
            nearest = bfs_nearest_safe_zone(self.graph, source_id, mobility)
            result["message"] = (
                f"Dijkstra found no route. BFS suggests {nearest} as the nearest safe zone, "
                f"but no costed path is available. Manual assessment is needed."
            )
            return result

        dest = self.graph.locations[path.target_id]
        accepted = dest.receive_evacuees(group_size)

        result["path"] = path
        result["message"] = (
            f"Route found: {' -> '.join(path.path)}. "
            f"{accepted}/{group_size} evacuees accepted at {dest.name}."
        )
        if accepted < group_size:
            result["message"] += f" {group_size - accepted} could not be placed because the safe zone is nearing capacity."

        self.plans.append(path)
        return result

    def plan_mass_evacuation(self, groups: list[dict]) -> list[dict]:
        priority_order = {
            MobilityType.INJURED: 0,
            MobilityType.ON_FOOT: 1,
            MobilityType.VEHICLE: 2,
        }
        sorted_groups = sorted(groups, key=lambda group: priority_order.get(group.get("mobility", MobilityType.VEHICLE), 2))

        return [
            self.plan_single_evacuation(
                source_id=group["source_id"],
                mobility=group.get("mobility", MobilityType.VEHICLE),
                group_size=group.get("size", 1),
            )
            for group in sorted_groups
        ]
