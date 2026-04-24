# Humanitarian Evacuation Route Planning System
**Capstone Project — Algorithmic Design for Crisis Response**

## 1. Description of the Project
- **PROBLEM CONTEXT**:
    In armed conflict zones, civilians must evacuate through road networks that are partially destroyed, blocked by hostilities, or controlled by armed groups. Aid organizations need to identify the SAFEST and FASTEST routes for mass evacuation under severe uncertainty.

- **REAL-WORLD CONSTRAINTS MODELED**:
    - Roads can be BLOCKED (impassable), DAMAGED (slow), or CLEAR
    - Each road segment has a DANGER SCORE (0–10) based on proximity to conflict, checkpoints, or recent incidents
    - Civilian groups have varying MOBILITY (on foot, vehicle, injured)
    - Safe zones have limited CAPACITY — once full, they reject new arrivals
    - The graph can be updated in real time as conditions change

- **DATA STRUCTURES**:
    - Graph: adjacency list (dict of dicts) for O(1) neighbor lookup
    - Priority Queue: min-heap (heapq) for Dijkstra's O((V+E) log V)
    - BFS Queue: collections.deque for O(1) popleft


## 2. Significance of the Project


## 3. Code Structure

```text
app.py
main.py
evacuation_system/
├── constants.py
├── models.py
├── graph.py
├── algorithms.py
├── planner.py
└── scenario.py
```

## 4. Algorithms

- **PRIMARY ALGORITHMS**:
    1. Dijkstra's Algorithm  — finds the lowest-cost evacuation path through
                               a weighted road graph (cost = danger + time)
    2. BFS (Breadth-First)   — finds ALL reachable safe zones within a given
                               number of hops (for when roads are unweighted
                               or weight data is unavailable)

## 5. Verification of Algorithms


## 6. Execution Results and Analysis

## 7. Conclusions

## 8. AI Usage

