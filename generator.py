import random

def generate_drunken_walk(rows, cols, max_steps=600):
    """
    Generates a map using the Drunken Walker (Random Walk) algorithm.
    0 = Wall
    1 = Floor
    """
    # 1. Initialize a grid full of Walls (0)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # 2. Start the "Walker" in the absolute center
    r, c = rows // 2, cols // 2
    grid[r][c] = 1  # Starting point is always floor
    
    # 3. The Walk Loop
    for i in range(max_steps):
        # Pick a random direction: Up, Down, Left, Right
        # format: (row_change, col_change)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        
        # Calculate the potential new position
        new_r, new_c = r + dr, c + dc
        
        # CONSTRAINT CHECK: Is this new position inside the grid?
        if 0 <= new_r < rows and 0 <= new_c < cols:
            # If valid, move the walker there
            r, c = new_r, new_c
            # Carve the floor
            grid[r][c] = 1
            
    return grid