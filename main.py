# Name: A* Pathfinding Algorithm
# Author: Ben Sailor
# Date: 2024-08-23
# Description: This program is an implementation of the A* pathfinding algorithm 
#              in a grid using Pygame.

import pygame
import sys
import heapq
from Node import Node

# Initialize Pygame
pygame.init()

# Define constants
WIDTH = 1000
ROWS, COLS = 15, 15         # Number of rows and columns in the grid
SQUARE_SIZE = WIDTH // COLS  # Size of each square
BG_COLOR, RED, GREEN, BLUE, BLACK = (255, 255, 255),(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 0, 0)           

screen = pygame.display.set_mode((WIDTH, WIDTH)) # Create the Pygame window
pygame.display.set_caption("Grid Clicker")

# Create a 3D matrix to store each square (Node object) in the grid
grid = [[Node(row, col, BG_COLOR=BG_COLOR, SQUARE_SIZE=SQUARE_SIZE) for col in range(COLS)] for row in range(ROWS)] 

for row in range(ROWS):             # Add neighbors to each node
    for col in range(COLS): 
        node = grid[row][col]       # Add all neighbors to the node in the below line.   
        neighbors = [grid[r][c] for r,c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)] if 0 <= r < ROWS and 0 <= c < COLS]
        node.neighbors = neighbors  # Neighbors are set to the Node object

def draw_grid():                    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col].draw(screen)


def get_square(pos):                # Get the square that was clicked
    x, y = pos                      # from the x and y coordinates
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def reconstruct_path(came_from, current):   # Reconstruct the path
    while current in came_from:     # Iterate through the came_from dictionary
        current = came_from[current]# move to the next node
        current.color = BLUE        # Change the color of the node to blue
        draw_grid()                 # Draw the grid and update the display
        pygame.display.flip()     

def a_star_search(start, end):      # A* search algorithm
    open_set = []                   # Initialize the open set
    heapq.heappush(open_set, (0, start))    # Add the start node to the open set
    came_from = {}                  # Initialize the came_from dictionary
    g_score = {node: float("inf") for row in grid for node in row}  # Initialize the g_score dictionary
    g_score[start] = 0              # Set the g_score of the start node to 0
    f_score = {node: float("inf") for row in grid for node in row}  # Initialize the f_score dictionary
    f_score[start] = start.heuristic(end)   # Set the f_score of the start node to the heuristic value

    while open_set:                 # While the open set is not empty
        _, current = heapq.heappop(open_set)    # Pop the node with the lowest f_score
                                    # and set it to current
        if current == end:          # If the current node is the end node
            reconstruct_path(came_from, current)    # Reconstruct the path and return True
            return True             

        for neighbor in current.neighbors:  # For each neighbor of the current node
            if neighbor.wall:       # If the neighbor is a wall, skip it
                continue            
            tentative_g_score = g_score[current] + 1 # IDEA: Could change the heuristic to be biased towards continuing in the same direction rather than changing direction

            if tentative_g_score < g_score[neighbor]:   # If the tentative g_score is less than the g_score of the neighbor
                came_from[neighbor] = current           # Set the neighbor's parent to the current node
                g_score[neighbor] = tentative_g_score   # Set the neighbor's g_score to the tentative g_score
                f_score[neighbor] = g_score[neighbor] + neighbor.heuristic(end) # Set the neighbor's f_score to the g_score + heuristic value
                if neighbor not in [i[1] for i in open_set]:    # If the neighbor is not in the open set
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))   # Add the neighbor to the open set
        draw_grid()                 # Draw the grid and update the display
        pygame.display.flip()
    return False                    # No path found

start_node = None                   # Initialize the start node
end_node = None                     # Initialize the end node

while True:                         # Main loop
    for event in pygame.event.get():# Check for events
        if event.type == pygame.QUIT:   # If the user closes the window
            pygame.quit()               # Quit Pygame and close the window
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:    # If the user clicks the mouse
            if event.button == 1:                   # and it is a left mouse click  
                pos = pygame.mouse.get_pos()        # Get the position of the mouse
                row, col = get_square(pos)          # Get the square that was clicked
                if start_node is None:              # If the start node has not been set 
                    grid[row][col].color = GREEN if grid[row][col].color == BG_COLOR else BG_COLOR
                    grid[row][col].start = True     # then this is the first click, 
                    start_node = grid[row][col]     # set the start node to the clicked square
                
                elif end_node is None:              # If the end node has not been set
                    if grid[row][col].start:        # and the clicked square is the start node
                        continue                    # then skip this square
                    grid[row][col].color = RED if grid[row][col].color == BG_COLOR else BG_COLOR
                    grid[row][col].end = True       # otherwise, set the end node to the clicked square
                    end_node = grid[row][col]       
                
                else:                               # If both the start and end nodes have been set
                    if grid[row][col].start or grid[row][col].end:  # and the clicked square is the start or end node
                        continue                    # then skip this square
                    grid[row][col].remove()         # otherwise, remove the square (Wall)
            
            elif event.button == 3:                 # if right mouse click
                a_star_search(start_node, end_node) # Run the A* search algorithm

    screen.fill(BG_COLOR)                           # Fill the screen with the background color
    
    draw_grid()                                     # Draw the grid
    
    pygame.display.flip()                           # Update the display
