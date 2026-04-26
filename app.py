"""Flask web app for the Humanitarian Evacuation Route Planning System."""

from flask import Flask, render_template, request

from evacuation_system import EvacuationPlanner, MobilityType, build_sample_scenario

app = Flask(__name__)


def serialize_path(path):
    if path is None:
        return None

    return {
        "route": " -> ".join(path.path),
        "distance": round(path.total_dist_km, 2),
        "time_hours": round(path.total_time_h, 2),
        "time_minutes": int(path.total_time_h * 60),
        "max_danger": round(path.max_danger, 2),
        "avg_danger": round(path.avg_danger, 2),
        "cost": round(path.total_cost, 4),
        "risk": "High Risk" if path.is_high_risk else "Acceptable Risk",
        "warnings": path.warnings,
        "nodes": path.path,
    }


def serialize_graph(graph, mobility, active_route=None):
    """Convert graph locations and roads into SVG-friendly coordinates."""
    active_route = active_route or []
    route_edges = {
        tuple(sorted((active_route[i], active_route[i + 1])))
        for i in range(len(active_route) - 1)
    }

    locations = list(graph.locations.values())
    min_lat = min(location.latitude for location in locations)
    max_lat = max(location.latitude for location in locations)
    min_lon = min(location.longitude for location in locations)
    max_lon = max(location.longitude for location in locations)

    width = 760
    height = 430
    padding = 55

    def scale_location(location):
        lon_range = max(max_lon - min_lon, 0.001)
        lat_range = max(max_lat - min_lat, 0.001)

        x = padding + ((location.longitude - min_lon) / lon_range) * (width - 2 * padding)
        y = height - padding - ((location.latitude - min_lat) / lat_range) * (height - 2 * padding)

        return round(x, 2), round(y, 2)

    node_lookup = {}
    nodes = []

    for location in locations:
        x, y = scale_location(location)
        node_lookup[location.id] = {"x": x, "y": y}

        nodes.append({
            "id": location.id,
            "name": location.name,
            "type": location.zone_type.value,
            "danger": location.danger_level,
            "x": x,
            "y": y,
        })

    roads = []
    seen_edges = set()

    for from_id, road_list in graph.adjacency.items():
        for road in road_list:
            edge_key = tuple(sorted((road.from_id, road.to_id)))

            if edge_key in seen_edges:
                continue

            seen_edges.add(edge_key)

            start = node_lookup[road.from_id]
            end = node_lookup[road.to_id]

            roads.append({
                "from_id": road.from_id,
                "to_id": road.to_id,
                "x1": start["x"],
                "y1": start["y"],
                "x2": end["x"],
                "y2": end["y"],
                "distance": road.distance_km,
                "danger": road.danger_score,
                "cost": round(road.composite_cost(mobility), 4),
                "status": road.status.value,
                "is_route": edge_key in route_edges,
            })

    return {
        "width": width,
        "height": height,
        "nodes": nodes,
        "roads": roads,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    graph = build_sample_scenario()
    planner = EvacuationPlanner(graph)

    sources = graph.get_civilian_zones()
    safe_zones = graph.get_safe_zones()

    result = None
    selected_source = "VILLAGE_A"
    selected_mobility = "vehicle"
    group_size = 80
    prefer_safety = True
    active_route = []

    if request.method == "POST":
        selected_source = request.form.get("source", "VILLAGE_A")
        selected_mobility = request.form.get("mobility", "vehicle")
        group_size = int(request.form.get("group_size", 1))
        prefer_safety = request.form.get("prefer_safety") == "on"

        mobility = MobilityType(selected_mobility)

        plan = planner.plan_single_evacuation(
            selected_source,
            mobility=mobility,
            group_size=group_size,
            prefer_safety=prefer_safety,
        )

        serialized_path = serialize_path(plan["path"])
        active_route = serialized_path["nodes"] if serialized_path else []

        result = {
            "message": plan["message"],
            "fallback": plan["fallback"],
            "path": serialized_path,
            "reachability": plan["reachability"],
        }

    mobility = MobilityType(selected_mobility)
    graph_view = serialize_graph(graph, mobility, active_route)

    return render_template(
        "index.html",
        graph=graph,
        graph_view=graph_view,
        sources=sources,
        safe_zones=safe_zones,
        result=result,
        selected_source=selected_source,
        selected_mobility=selected_mobility,
        group_size=group_size,
        prefer_safety=prefer_safety,
    )


if __name__ == "__main__":
    app.run(debug=True)