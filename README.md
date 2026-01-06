# Logistics Route Optimizer

A **visual logistics simulation** built with **Python and Pygame** that generates a city map, places houses, roads, highways, obstacles, and simulates a delivery van finding optimal routes using **Dijkstra's algorithm**.

This project demonstrates **grid-based pathfinding** and allows **dynamic traffic simulation**.

---

## Features

- Procedurally generated **city map** with roads, highways, and obstacles.  
- Randomly placed **houses** as delivery destinations.  
- **Dijkstra's algorithm** for shortest path calculation.  
- Visual **simulation of a delivery van** moving through the city.  
- **Interactive traffic creation**: Drag on roads to simulate congestion.  
- Displays **current position and total cost** in real-time.

---

## How It Works

1. **City Generation**
   - Grid-based map (`ROWS x COLS`) is initialized as plain terrain.
   - Maze-like road network is generated using recursive backtracking.
   - Two highways are added horizontally and vertically.
   - Random obstacles are placed to increase pathfinding complexity.
   - Houses are placed adjacent to roads for deliveries.

2. **Pathfinding**
   - Dijkstra's algorithm calculates the **shortest path** from the warehouse to selected houses.
   - The van moves along the computed path in real-time.
   - Users can select multiple houses to generate a **multi-destination route**.

3. **Traffic Simulation**
   - Users can **click and drag on roads** to simulate traffic.
   - Roads with traffic increase travel cost, affecting the computed path dynamically.

---

## Controls

- **Click on a house** → select it as a delivery target.  
- **Press SPACE** → compute and start the delivery route.  
- **Click & drag on roads** → simulate traffic.  
- **Close window** → exit the simulation.

---

## Grid Legend

| Type      | Color        |
|-----------|--------------|
| Road      | White        |
| Highway   | Orange       |
| Plain     | Tan          |
| House     | Green        |
| Obstacle  | Dark Orange  |
| Selected  | Blue         |
| Path      | Light Blue   |
| Traffic   | Gray         |

---

## Requirements

- Python 3.x  
- Pygame library  

Install Pygame via pip:

```bash
pip install pygame
