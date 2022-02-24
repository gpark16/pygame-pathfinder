--- PathFinder ---

This a pathfinding app which uses the A* Algorithm to find the most optimal path between a start and an end node. Implemented in python and uses Pygame for the custom GUI

--- Need installed for use ---

Python 3
Pygame

--- How to use ---

Navigate to the directory containing the file in the terminal/command-line

Enter "python3 pathfinder.py" and press enter

Left Click to place the start/end nodes and barriers

Right Click to reset any nodes to blank

Spacebar to run the pathfinding algorithm

C to clear the board

--- Notes ---

#h(n) is the "absolute distance" heuristic. We are using Manhattan Distances for this
#g(n) is the current shortest distance from the start node to the current node
#f(n) is h(n) + g(n)
#Every node has an f(n) and we will consider the f(n) of the possible next nodes to know which path to move toward
