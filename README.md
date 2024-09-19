Features:
Grid-Based Pathfinding: Visualizes the search process on a 50x50 grid.
Interactive Controls:
Set start and target points with mouse clicks.
Draw walls/obstacles by dragging the mouse.
Algorithm Options:
Dijkstra's Algorithm: Uses a priority queue to find the shortest path from the start to the target.
Breadth-First Search (BFS): Simple, unweighted pathfinding method (commented out for reference).
Visual Feedback: Colors represent different states of the grid cells:
Red: Cells currently in the queue.
Green: Cells that have been visited.
Blue: The path from start to target.
Black: Walls/obstacles.
Yellow: Target cell.
Cyan: Start cell.
Getting Started
Prerequisites
Python 3.x
Pygame library: Install using pip install pygame
Tkinter library (for message boxes): Comes pre-installed with most Python distributions.
