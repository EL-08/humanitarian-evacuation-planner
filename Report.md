# HUMANITARIAN EVACUATION ROUTE PLANNING SYSTEM
## Capstone Project Report

---

## 1. Description of the Project
Given a conflict-zone road network, the system computes evacuation routes that balance **travel time** and **danger exposure**. Locations (villages, checkpoints, safe zones) are modeled as nodes, and roads as weighted edges with dynamic attributes (status, danger).

The system supports:
- Optimal pathfinding to safe zones (Dijkstra)
- Reachability analysis under uncertainty (BFS)
- Capacity-aware evacuation planning (safe zones can fill)

Input: 
- graph
- source location
- mobility type

Output: 
- evacuation route 
- risk/time metrics
- warnings  

---

## 2. Significance of the Project
This models real humanitarian constraints:
- Incomplete/dynamic information (roads change status)
- Resource limits (safe zone capacity)
- Trade-offs (fast vs safe routes)

Novel aspects:
- Composite cost function combining normalized time and danger  
- Fallback strategies (BFS when optimal routing fails)  
- Real-time updates (road destruction, congestion)

---

## 3. Code Structure
```text
humanitarian_evacuation_route_planner/
├── app.py                         # Flask web application
├── main.py                        # Command-line demo
├── requirements.txt               # Python dependencies
├── README.md                      # Project instructions
├── Report.md                      # Draft project report
├── evacuation_system/
│   ├── __init__.py
│   ├── constants.py               # Enums and shared constants
│   ├── models.py                  # Data models
│   ├── graph.py                   # Evacuation graph class
│   ├── algorithms.py              # Dijkstra and BFS helper functions
│   ├── planner.py                 # High-level evacuation planner
│   └── scenario.py                # Sample scenario builder
├── templates/
│   └── index.html                 # Web UI template
├── static/
│   └── style.css                  # Web UI styling
└── tests/
    └── test_algorithms.py         # Basic algorithm tests
```
Flow:
Scenario builds graph → Planner runs BFS → Dijkstra → Outputs structured results

---

## 4. Description of Algorithms

### Dijkstra’s Algorithm
- Cost = 0.6(time) + 0.4(danger)
- Uses priority queue (min-heap)
- Avoids blocked and high-danger paths

Time Complexity: O((V + E) log V)

---

### BFS (Breadth-First Search)
Used for:
- Reachability
- Fallback routing

Time Complexity: O(V + E)

---

## 5. Verification of Algorithms
Example:
A → B (safe), A → C (dangerous), B → D (safe zone)

Dijkstra selects A → B → D due to lower risk.
BFS confirms D is reachable.

---

## 6. Execution Results and Analysis
- Vehicle routes prioritize safety and speed balance
- On-foot routes increase time weight
- Dynamic updates trigger rerouting

Observations:
- Mobility impacts path selection
- System adapts to changing conditions
- Capacity constraints affect 

---

## 7. AI Usage
AI assisted with:
- Structuring project
- Refactoring code

Core algorithms were manually designed and verified.

---

## 8. Conclusion
- Dijkstra effective with composite cost
- BFS useful fallback
- Trade-offs unavoidable (safety vs speed)

Limitations:
- Static danger scores
- No congestion modeling
- Simplified geography

Application of Course Learning:
- Priority queue / min-heap
- Algorithm design and complexity analysis
- Trade-off reasoning

The system shows that Dijkstra can be adapted with a composite cost function to balance safety and efficiency, while BFS provides reliable fallback under uncertainty. Results highlight how constraints like road conditions, mobility differences, and safe zone capacity directly impact route selection and feasibility. Key limitations include static danger modeling, lack of congestion handling, and simplified real-world assumptions. Overall, the project demonstrates practical application of graph algorithms, complexity analysis, and trade-off reasoning in a real-world crisis scenario.

---

## Contributions
- Michael: Creating the beta and final main code. Writing part of the report.
- Eric: Creating the UI, the github page, the sample inputs, and the MD's. Reorganizing the main code.
