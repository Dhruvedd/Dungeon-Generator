import random

def generate_cave(rows, cols, iterations=5, fill_percent=0.50, input_grid=None):
    """
    Generates or smooths a cave using Cellular Automata.
    - If input_grid is None: Starts with random noise.
    - If input_grid is provided: Smooths that grid instead.
    """
    # 1. INITIALIZATION
    if input_grid is None:
        # Start from scratch with random noise
        grid = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                    row.append(0) 
                else:
                    if random.random() < fill_percent:
                        row.append(0)
                    else:
                        row.append(1)
            grid.append(row)
    else:
        # Start with the provided grid (copy it)
        grid = [row[:] for row in input_grid]

    # 2. ITERATIVE SMOOTHING
    for i in range(iterations):
        grid = apply_automata_rules(grid, rows, cols)
        
    return grid

def apply_automata_rules(old_grid, rows, cols):
    """
    Standard 4-5 Rule:
    - 4 or more wall neighbors -> Become Wall
    - Less than 4 -> Become Floor
    """
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            # Border walls are mandatory
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                new_grid[r][c] = 0
                continue

            wall_neighbors = count_walls(old_grid, r, c, rows, cols)
            
            # The "Smoothing" Logic
            if wall_neighbors >= 5: # If surrounded by walls, be a wall
                new_grid[r][c] = 0
            elif wall_neighbors <= 3: # If surrounded by space, be floor
                 new_grid[r][c] = 1
            else:
                # If it's 4, keep state (prevents flickering)
                new_grid[r][c] = old_grid[r][c]
                
    return new_grid

def count_walls(grid, r, c, rows, cols):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            
            nr, nc = r + i, c + j
            
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                count += 1
            elif grid[nr][nc] == 0:
                count += 1
    return count