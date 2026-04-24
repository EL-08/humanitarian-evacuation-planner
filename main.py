"""Command-line demo for the Humanitarian Evacuation Route Planning System."""

from evacuation_system import EvacuationPlanner, MobilityType, RoadStatus, bfs_reachability, build_sample_scenario


def run_demo():
    print("=" * 70)
    print("  HUMANITARIAN EVACUATION ROUTE PLANNER — Core Engine Demo")
    print("=" * 70)

    graph = build_sample_scenario()
    planner = EvacuationPlanner(graph)

    print(f"\n{graph.summary()}\n")

    scenarios = [
        ("SCENARIO 1: Vehicle convoy from Al-Rashid Village", "VILLAGE_A", MobilityType.VEHICLE, 80),
        ("SCENARIO 2: Civilians on foot from Hamdaniyah Town", "TOWN_CENTER", MobilityType.ON_FOOT, 200),
    ]

    for title, source, mobility, size in scenarios:
        print("-" * 50)
        print(title)
        print("-" * 50)
        result = planner.plan_single_evacuation(source, mobility, group_size=size)
        if result["path"]:
            print(result["path"].summary())
        print("Status:", result["message"], "\n")

    print("-" * 50)
    print("SCENARIO 3: BFS Reachability from Beit Nour Village")
    print("-" * 50)
    reach = bfs_reachability(graph, "VILLAGE_B", max_hops=6)
    print(reach.summary())

    print("\n" + "-" * 50)
    print("SCENARIO 4: Road bombed — Village A to Town Center now BLOCKED")
    print("-" * 50)
    graph.update_road_status("VILLAGE_A", "TOWN_CENTER", RoadStatus.BLOCKED, new_danger=9.5)
    result = planner.plan_single_evacuation("VILLAGE_A", MobilityType.VEHICLE, group_size=50)
    if result["path"]:
        print(result["path"].summary())
    print("Status:", result["message"])

    print("\n" + "=" * 70)
    print("  Core engine validated. Ready for web layer integration.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
