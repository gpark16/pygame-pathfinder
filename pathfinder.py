from tkinter import Y
import pygame
import math

from queue import PriorityQueue

#Initialize a window for display
width = 800
win = pygame.display.set_mode((width, width))

pygame.display.set_caption("A* Pathfinding Algorithm")

#Color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == YELLOW

    def is_open(self):
        return self.color == ORANGE
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_open(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = YELLOW

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = BLUE

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #Check Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #Check Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Check Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #Check Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#Define the heuristic function
def h(p1, p2): 
    #Manhattan distance will be the "L" distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Traverse from the end node back to the start node in the most efficient path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#A* Algorithm
def a_star_algorithm(draw, grid, start, end):
    count = 0 #Used to keep track of the index of the nodes
    open_set = PriorityQueue()

    open_set.put((0, count, start)) #Insert the first node with its F(n) and index: [F(n), index, node]
    came_from = {} #Keeping track of the path

    g_n = {node: float("inf") for row in grid for node in row} #Initialize the G(n) for all nodes as infinity
    g_n[start] = 0

    f_n = {node: float("inf") for row in grid for node in row} #Initialize the F(n) for all nodes as infinity
    f_n[start] = h(start.get_pos(), end.get_pos()) #Initialize the F(n) for the start node as the heuristic function value

    open_set_hash = {start}

    while not open_set.empty(): #The algorithm will run until the open_set is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] #Get the current node
        open_set_hash.remove(current)

        if current == end: #Outline optimal path if the end node is found
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors: #If the end is not found, take into consideration all the neighbors
            temp_g_n = g_n[current] + 1

            if temp_g_n < g_n[neighbor]: #If the new G(n) is less the the old G(n), update the value for the better path
                came_from[neighbor] = current
                g_n[neighbor] = temp_g_n
                f_n[neighbor] = temp_g_n + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash: #If the neighbors are not in the open_set_hash, add them
                    count += 1
                    open_set.put((f_n[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
        
    return False

#Create the 2d array and fill it with nodes
def make_grid(rows, width):
    grid = []
    gap = width // rows #Width of each node

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

#Drawing the lines for the grid to visually distinguish the nodes
def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) #Horizontal lines for grid
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) #Vertical lines for grid

#Main draw function which constructs the display
def draw(win, grid, rows, width):
    win.fill(WHITE) #fills the entire screen with one color at the beginning of each frame
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width) #Draws the grid lines on top of the initialized window
    pygame.display.update()

#Figure out the position of the mouse within the grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    rows = 50 #Correlates to number of nodes
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started: #If the algorithm is running, only allow the user to quit
                continue

            if pygame.mouse.get_pressed()[0]: #Checks for left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                
                node = grid[row][col]
                
                if not start and node != end: #If the start doesn't exist, create the start node in the current mouse position
                    start = node
                    start.make_start()

                elif not end and node != start: #If the end doesn't exist, create the start node in the current mouse position
                    end = node
                    end.make_end()
                
                elif node != end and node != start: #If both start and end exist, create a barrier in the current mouse position
                    node.make_barrier()
            
            elif pygame.mouse.get_pressed()[2]: #Checks for right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                
                node = grid[row][col]

                node.reset() #Reset any node that has been right-clicked

                if node == start:
                    start = None

                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN: #If space is pressed, begin the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star_algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                
                if event.key == pygame.K_c: #Resets the grid
                    start = None
                    end = None
                    grid = make_grid(rows, width)

                
    
    pygame.quit()

main(win, width)