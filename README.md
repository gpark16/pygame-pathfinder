--- PathFinder ---
This a pathfinding app which uses the A* Algorithm to find the most optimal path between a start and an end node. Implemented in python and uses Pygame for the custom GUI

--- How to use ---



--- Notes ---
#h(n) is the "absolute distance" heuristic. We are using Manhattan Distances for this
#g(n) is the current shortest distance from the start node to the current node
#f(n) is h(n) + g(n)
#Every node has an f(n) and we will consider the f(n) of the possible next nodes to know which path to move toward