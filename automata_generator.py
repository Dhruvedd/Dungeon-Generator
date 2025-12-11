import random

def generate_cave(rows, cols, iterations=5, fill_percent=0.48):
    """
    Generates a cave using Cellular Automata (Constraint Satisfaction).
    1. Fill map with random noise (50% chance of wall).
    2. Apply smoothing rules (Constraints) multiple times.
    """
    # 1. INITIALIZATION (Random Noise)
    # We create a grid where every tile has a fill_percent chance to be a Wall (0)
    # and a 1-fill_percent chance to be a Floor (1).
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            # Border walls are mandatory constraint
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                row.append(0) 
            else:
                # 45% chance of wall
                if random.random() < fill_percent:
                    row.append(0)
                else:
                    row.append(1)
        grid.append(row)

    # 2. ITERATIVE SMOOTHING (The AI/Constraint Step)
    # We apply the rules multiple times to smooth the cave.
    for i in range(iterations):
        grid = apply_automata_rules(grid, rows, cols)
        
    return grid

def apply_automata_rules(old_grid, rows, cols):
    """
    Creates a new grid based on neighbor constraints.
    Rule: "If I have more than 4 wall neighbors, I become a wall."
    """
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            # 1. Count Wall Neighbors (Constraint Check)
            wall_neighbors = count_walls(old_grid, r, c, rows, cols)
            
            # 2. Apply Logic
            # "The 4-5 Rule":
            # If a tile has > 4 wall neighbors, it BECOMES a wall (clustered).
            # If it has < 4, it BECOMES a floor (open space).
            if wall_neighbors > 4:
                new_grid[r][c] = 0 # Wall
            else:
                new_grid[r][c] = 1 # Floor
                
    return new_grid

def count_walls(grid, r, c, rows, cols):
    """Helper to count walls around a tile (including diagonals)."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Don't check yourself
            if i == 0 and j == 0:
                continue
            
            neighbor_r = r + i
            neighbor_c = c + j
            
            # Check bounds (off-screen counts as wall)
            if neighbor_r < 0 or neighbor_r >= rows or neighbor_c < 0 or neighbor_c >= cols:
                count += 1
            elif grid[neighbor_r][neighbor_c] == 0:
                count += 1
    return count