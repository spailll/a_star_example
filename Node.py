import pygame

GRID_COLOR = (0, 0, 0)      # Grid color (black)

class Node:                 # Node class
    def __init__(self, row, col, BG_COLOR=(255, 255, 255), SQUARE_SIZE=20):
        self.row = row      # Row of the node
        self.col = col      # Column of the node
        self.color=BG_COLOR # Color of the node
        self.SQUARE_SIZE=SQUARE_SIZE    # Size of the square
        self.wall = False   # Wall flag
        self.start = False  # Start flag
        self.end = False    # End flag
        self.neighbors = [] # Neighbors of the node
        self.parents = None # Parent of the node

    def __lt__(self, other):    # Less than operator (for direct comparison)
        return False           

    def add_neighbor(self, node):   # Add a neighbor to the node
        self.neighbors.append(node) 

    def remove_neighbor(self, neighbor):# Remove a neighbor from the node
        if neighbor in self.neighbors:   
            self.neighbors.remove(neighbor) 
        
    def remove(self):           # Function to remove a node from a graph 
        self.color = (0, 0, 0)  # (doesn't remove it from the board, just the graph datastructure)
        for neighbor in self.neighbors: 
            neighbor.remove_neighbor(self)  
        self.neighbors = []     
        self.color = (0,0,0)    
        self.wall = True        

    def draw(self, screen):             # Draw the node
        pygame.draw.rect(screen, self.color, (self.col * self.SQUARE_SIZE, self.row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
        pygame.draw.rect(screen, GRID_COLOR, (self.col * self.SQUARE_SIZE, self.row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

    def heuristic(self, other):        # Heuristic function, Manhattan distance 
        return abs(self.row - other.row) + abs(self.col - other.col)
    
    def f_score(self, g_score, end_node):   # F score function to return g_score + heuristic
        return g_score[self] + self.heuristic(end_node)