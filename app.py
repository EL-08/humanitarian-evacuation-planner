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
        result = {
            "message": plan["message"],
            "fallback": plan["fallback"],
            "path": serialize_path(plan["path"]),
            "reachability": plan["reachability"],
        }

    return render_template(
        "index.html",
        graph=graph,
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
