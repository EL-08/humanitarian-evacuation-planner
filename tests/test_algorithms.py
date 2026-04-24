from evacuation_system import MobilityType, bfs_reachability, build_sample_scenario, dijkstra


def test_dijkstra_finds_route_to_safe_zone():
    graph = build_sample_scenario()
    path = dijkstra(graph, "VILLAGE_A", "UN_COMPOUND", MobilityType.VEHICLE)
    assert path is not None
    assert path.source_id == "VILLAGE_A"
    assert path.target_id == "UN_COMPOUND"
    assert path.total_dist_km > 0


def test_bfs_finds_reachable_safe_zones():
    graph = build_sample_scenario()
    result = bfs_reachability(graph, "VILLAGE_B", max_hops=6)
    assert "VILLAGE_B" in result.reachable
    assert len(result.reachable_safe) > 0
