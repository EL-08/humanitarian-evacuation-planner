

## Main Algorithms

- **Dijkstra's Algorithm**: Finds the lowest-cost evacuation route using a composite cost based on travel time and danger.
- **Breadth-First Search (BFS)**: Finds reachable safe zones when weighted road data is unavailable or when a fast reachability check is needed.

## Project Structure

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

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the web app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Run the command-line demo:

```bash
python main.py
```

Run tests:

```bash
pytest
```
